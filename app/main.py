from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import Base, engine
from .routers import tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Task Manager API",
    description="CRUD API для управления задачами. Статусы: created, in_progress, completed.",
    version="1.0.0",
    contact={"name": "Task Manager", "url": "https://example.com"},
    lifespan=lifespan,
)

app.include_router(tasks.router)
