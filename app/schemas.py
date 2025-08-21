
from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

class TaskStatus(str, Enum):
    created = "created"
    in_progress = "in_progress"
    completed = "completed"

class TaskCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.created

class TaskUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None

class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    name: str
    description: Optional[str]
    status: TaskStatus

class TaskList(BaseModel):
    total: int
    items: list[TaskRead]
