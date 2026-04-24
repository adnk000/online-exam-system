import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from app.database.session import SessionLocal
from app.models.user import User
from app.models.question import Question
from app.core.security import hash_password, encrypt_answer


def seed_data() -> None:
    db = SessionLocal()

    # Users
    users = [
        {"email": "student1@test.com", "password": "1234"},
        {"email": "student2@test.com", "password": "1234"},
        {"email": "student3@test.com", "password": "1234"},
        {"email": "admin@test.com", "password": "admin123"},
    ]

    for u in users:
        existing = db.query(User).filter(User.email == u["email"]).first()
        if not existing:
            db.add(User(
                email=u["email"],
                password=hash_password(u["password"]),
                role="admin" if u["email"] == "admin@test.com" else "student"
            ))

    # Questions
    questions = [
        {
            "question_text": "What is 2 + 2?",
            "option_a": "3",
            "option_b": "4",
            "option_c": "5",
            "option_d": "6",
            "correct_answer": "4",
        },
        {
            "question_text": "Capital of India?",
            "option_a": "Mumbai",
            "option_b": "Delhi",
            "option_c": "Chennai",
            "option_d": "Kolkata",
            "correct_answer": "Delhi",
        },
        {
            "question_text": "Which is a programming language?",
            "option_a": "HTML",
            "option_b": "CSS",
            "option_c": "Python",
            "option_d": "Photoshop",
            "correct_answer": "Python",
        },
    ]

    for q in questions:
        existing = db.query(Question).filter(
            Question.question_text == q["question_text"]
        ).first()
        if not existing:
            db.add(Question(
                question_text=q["question_text"],
                option_a=q["option_a"],
                option_b=q["option_b"],
                option_c=q["option_c"],
                option_d=q["option_d"],
                correct_answer=encrypt_answer(q["correct_answer"])
            ))

    db.commit()
    db.close()
    print("Seed data inserted!")


if __name__ == "__main__":
    seed_data()
