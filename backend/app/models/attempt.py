from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from app.database.session import Base

class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String)
    score = Column(Integer)
    total = Column(Integer)
    start_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))