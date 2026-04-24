from fastapi import FastAPI

from app.database.session import Base, engine

# 🔥 Import ALL models FIRST (very important)
import app.models.user
import app.models.question
import app.models.answer
import app.models.attempt

# 🔥 Import routers
from app.api.routes.auth import router as auth_router
from app.api.routes import question, admin

# 🔥 Create app
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for now (dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend running 🚀"}

# 🔥 Create tables
Base.metadata.create_all(bind=engine)

# 🔥 Include routers
app.include_router(auth_router)
app.include_router(question.router)
app.include_router(admin.router)


from app.database.session import SessionLocal
from app.models.user import User
from app.models.question import Question

@app.on_event("startup")
def seed_data():
    db = SessionLocal()

    # 👨‍🎓 Users
    if not db.query(User).first():
        db.add(User(email="student1@test.com", password="1234"))
        db.add(User(email="student2@test.com", password="1234"))
        db.add(User(email="admin@test.com", password="admin123"))

    # 🧠 Questions
    if not db.query(Question).first():
        db.add(Question(
            question_text="What is 2 + 2?",
            option_a="3",
            option_b="4",
            option_c="5",
            option_d="6",
            correct_option="4"
        ))

        db.add(Question(
            question_text="Capital of India?",
            option_a="Mumbai",
            option_b="Delhi",
            option_c="Chennai",
            option_d="Kolkata",
            correct_option="Delhi"
        ))

    db.commit()
    db.close()