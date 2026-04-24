from pydantic import BaseModel
from typing import List

class AnswerItem(BaseModel):
    question_id: int
    selected_option: str

class SubmitExam(BaseModel):
    answers: List[AnswerItem]