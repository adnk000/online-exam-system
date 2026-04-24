from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.models.attempt import Attempt
from app.models.answer import Answer
from app.api.routes.auth import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin"])


# 🔌 DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔐 Admin check
def admin_only(user):
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only access")


# 📊 Get all attempts
@router.get("/attempts")
def get_all_attempts(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    admin_only(user)

    attempts = db.query(Attempt).all()

    return {
        "total_attempts": len(attempts),
        "data": attempts
    }


# 👤 Get specific user's attempt
@router.get("/attempt/{email}")
def get_user_attempt(
    email: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    admin_only(user)

    attempt = db.query(Attempt).filter(Attempt.user_email == email).first()

    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")

    return attempt


# 🧠 Get user's answers
@router.get("/answers/{email}")
def get_user_answers(
    email: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    admin_only(user)

    answers = db.query(Answer).filter(Answer.user_email == email).all()

    return {
        "total_answers": len(answers),
        "data": answers
    }


# 🏆 Top students (Admin only)
@router.get("/top")
def top_students(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    admin_only(user)

    top = db.query(Attempt)\
        .order_by(Attempt.score.desc(), Attempt.total.desc())\
        .limit(5)\
        .all()

    return {
        "top_students": top
    }


# 🌍 Public leaderboard (for frontend UI)
@router.get("/leaderboard")
def public_leaderboard(db: Session = Depends(get_db)):
    results = db.query(Attempt)\
        .order_by(Attempt.score.desc(), Attempt.total.desc())\
        .all()

    return [
        {
            "user_email": r.user_email,
            "score": r.score,
            "total": r.total
        }
        for r in results
    ]