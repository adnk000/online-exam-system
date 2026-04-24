from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from app.database.session import SessionLocal
from app.models.question import Question
from app.models.attempt import Attempt
from app.models.answer import Answer

from app.schemas.question_schema import QuestionCreate, QuestionOut
from app.schemas.answer_schema import SubmitExam

from app.core.security import encrypt_answer, decrypt_answer
from app.api.routes.auth import get_current_user

router = APIRouter()

# ⏱ Exam duration (minutes)
EXAM_DURATION_MINUTES = 1   # change later (e.g., 60)


# 🔌 Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔥 Add Question (Admin Only)
@router.post("/questions")
def create_question(
    q: QuestionCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # 🔐 Admin check
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Only admin can add questions")

    # 🚫 Prevent duplicate questions
    existing_q = db.query(Question).filter(
        Question.question_text == q.question_text
    ).first()

    if existing_q:
        raise HTTPException(status_code=400, detail="Question already exists")

    # 🔒 Encrypt correct answer
    data = q.model_dump()
    data["correct_answer"] = encrypt_answer(data["correct_answer"])

    new_q = Question(**data)
    db.add(new_q)
    db.commit()

    return {"message": "Question added successfully"}


# 🔥 Get Questions
@router.get("/questions", response_model=list[QuestionOut])
def get_questions(db: Session = Depends(get_db)):
    return db.query(Question).all()


# 🔥 Submit Exam (Anti-Cheat + Timer)
@router.post("/submit-exam")
def submit_exam(
    data: SubmitExam,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    user_email = user["sub"]

    # 🔍 Get existing attempt
    attempt = db.query(Attempt).filter(
        Attempt.user_email == user_email
    ).first()

    # 🚫 Already submitted
    if attempt and attempt.score is not None:
        raise HTTPException(status_code=400, detail="You already submitted the exam")

    # ⏱ Timer check
    if attempt:
        end_time = attempt.start_time + timedelta(minutes=EXAM_DURATION_MINUTES)

        if datetime.now(timezone.utc) > end_time:
            raise HTTPException(status_code=400, detail="Time is up!")

    score = 0
    total = 0

    valid_options = ["option_a", "option_b", "option_c", "option_d"]

    for ans in data.answers:
        question = db.query(Question).filter(
            Question.id == ans.question_id
        ).first()

        if not question or not question.correct_answer:
            continue

        # 🚫 Invalid option check
        if ans.selected_option not in valid_options:
            continue

        total += 1

        correct = decrypt_answer(question.correct_answer)
        selected_text = getattr(question, ans.selected_option, None)

        # 🧠 Store answer key, not the option text
        db_answer = Answer(
            question_id=ans.question_id,
            selected_option=ans.selected_option,
            user_email=user_email
        )
        db.add(db_answer)

        if selected_text == correct:
            score += 1

    # 🛡 Create new attempt (start time now)
    attempt = Attempt(
        user_email=user_email,
        score=score,
        total=total,
        start_time=datetime.now(timezone.utc)
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    # 📊 Percentage
    percentage = (score / total) * 100 if total > 0 else 0

    return {
        "score": score,
        "total": total,
        "percentage": round(percentage, 2),
        "message": "Exam submitted successfully"
    }


# 🏆 Leaderboard (Top 10)
@router.get("/leaderboard")
def leaderboard(db: Session = Depends(get_db)):
    attempts = db.query(Attempt).order_by(
        Attempt.score.desc()
    ).limit(10).all()

    result = []

    for a in attempts:
        result.append({
            "user": a.user_email,
            "score": a.score,
            "total": a.total
        })

    return result