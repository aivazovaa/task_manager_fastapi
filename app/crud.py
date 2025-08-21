
import uuid
from typing import Optional, Sequence, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from . import models
from .schemas import TaskStatus

def create_task(db: Session, name: str, description: Optional[str], status: TaskStatus) -> models.Task:
    task = models.Task(id=str(uuid.uuid4()), name=name, description=description, status=status.value)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_task(db: Session, task_id: str) -> Optional[models.Task]:
    return db.get(models.Task, task_id)

def list_tasks(db: Session, status: Optional[TaskStatus], q: Optional[str], limit: int, offset: int) -> Tuple[int, Sequence[models.Task]]:
    stmt = select(models.Task)
    if status is not None:
        stmt = stmt.where(models.Task.status == status.value)
    if q:
        like = f"%{q}%"
        stmt = stmt.where(models.Task.name.ilike(like))
    total_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.execute(total_stmt).scalar_one()
    items = db.execute(stmt.order_by(models.Task.name).limit(limit).offset(offset)).scalars().all()
    return total, items

def update_task(db: Session, task: models.Task, name: Optional[str], description: Optional[str], status: Optional[TaskStatus]) -> models.Task:
    if name is not None:
        task.name = name
    if description is not None:
        task.description = description
    if status is not None:
        task.status = status.value
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task: models.Task) -> None:
    db.delete(task)
    db.commit()
