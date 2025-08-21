
from sqlalchemy import Column, String, Text, CheckConstraint
from .database import Base

ALLOWED_STATUSES = ("created", "in_progress", "completed")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, index=True)
    __table_args__ = (
        CheckConstraint(f"status in {ALLOWED_STATUSES}", name="status_check"),
    )
