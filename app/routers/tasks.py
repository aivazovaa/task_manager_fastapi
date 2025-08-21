
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from ..database import SessionLocal
from .. import crud, models, schemas

router = APIRouter(prefix="/tasks", tags=["Задачи"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("", response_model=schemas.TaskRead, status_code=status.HTTP_201_CREATED, summary="Создать задачу")
def create_task(payload: schemas.TaskCreate, db: Session = Depends(get_db)):
    task = crud.create_task(db, name=payload.name, description=payload.description, status=payload.status)
    return task

@router.get("/{task_id}", response_model=schemas.TaskRead, summary="Получить задачу по ID")
def get_task(task_id: str, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task

@router.get("", response_model=schemas.TaskList, summary="Список задач с фильтрацией и пагинацией")
def list_tasks(
    status_filter: schemas.TaskStatus | None = Query(default=None, alias="status"),
    q: str | None = None,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    total, items = crud.list_tasks(db, status=status_filter, q=q, limit=limit, offset=offset)
    return {"total": total, "items": items}

@router.put("/{task_id}", response_model=schemas.TaskRead, summary="Обновить задачу")
def update_task(task_id: str, payload: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    task = crud.update_task(db, task, name=payload.name, description=payload.description, status=payload.status)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить задачу")
def delete_task(task_id: str, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    crud.delete_task(db, task)
    return None
