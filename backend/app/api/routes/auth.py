from fastapi.security import HTTPBearer , HTTPAuthorizationCredentials
from fastapi import APIRouter, Depends, HTTPException, status , Header
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token , verify_token
from app.schemas.user_schema import UserCreate

router = APIRouter()
security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- REGISTER ----------------
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    
    # check duplicate BEFORE insert
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = User(
        email=user.email,
        password=hash_password(user.password),
        role="student"
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    return {"message": "User registered successfully"}


# ---------------- LOGIN ----------------
@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

from fastapi import Header

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    
    token = credentials.credentials
    payload = verify_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return payload
@router.get("/profile")
def profile(user=Depends(get_current_user)):
    return {"message": f"Welcome {user['sub']}"}





