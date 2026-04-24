from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.session import Base

class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer)
    selected_option = Column(String)
    user_email = Column(String)

    