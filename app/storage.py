from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from app.business_rules import is_task_overdue
from app.models import TaskCreate, TaskResponse, TaskUpdate


_tasks: dict[str, TaskResponse] = {}


def add_task(payload: TaskCreate) -> TaskResponse:
    now = datetime.now(timezone.utc)

    task = TaskResponse(
        id=str(uuid4()),
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        due_date=payload.due_date,
        tags=payload.tags,
        created_at=now,
        updated_at=now,
    )

    _tasks[task.id] = task
    return task


def get_all_tasks(
    status=None,
    priority=None,
    overdue: Optional[bool] = None,
    tag: Optional[str] = None,
) -> list[TaskResponse]:
    tasks = list(_tasks.values())

    if status is not None:
        tasks = [
            task
            for task in tasks
            if task.status == status
        ]

    if priority is not None:
        tasks = [
            task
            for task in tasks
            if task.priority == priority
        ]

    if overdue is not None:
        tasks = [
            task
            for task in tasks
            if is_task_overdue(
                due_date=task.due_date,
                task_status=task.status,
            )
            == overdue
        ]

    if tag is not None:
        cleaned_tag = tag.strip()

        tasks = [
            task
            for task in tasks
            if cleaned_tag in task.tags
        ]

    return tasks


def get_task_by_id(
    task_id: str,
) -> Optional[TaskResponse]:
    return _tasks.get(task_id)


def update_task(
    task_id: str,
    payload: TaskUpdate,
) -> Optional[TaskResponse]:
    task = _tasks.get(task_id)

    if task is None:
        return None

    updates = payload.model_dump(
        exclude_unset=True
    )

    if updates:
        updates["updated_at"] = (
            datetime.now(timezone.utc)
        )

        task = task.model_copy(
            update=updates
        )

        _tasks[task_id] = task

    return task


def delete_task(task_id: str) -> bool:
    if task_id not in _tasks:
        return False

    del _tasks[task_id]
    return True


def _reset() -> None:
    _tasks.clear()