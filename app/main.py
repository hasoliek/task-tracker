from datetime import datetime, timezone

from fastapi import FastAPI, status

from app import storage
from app.models import TaskCreate, TaskResponse


app = FastAPI(
    title="Task Tracker API",
    description="Minimal FastAPI skeleton for Module 1",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["tasks"],
)
def create_task(payload: TaskCreate) -> TaskResponse:
    return storage.add_task(payload)