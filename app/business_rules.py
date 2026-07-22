from datetime import date

from fastapi import HTTPException, status

from app.models import TaskStatus


_ALLOWED_TRANSITIONS: dict[TaskStatus, set[TaskStatus]] = {
    TaskStatus.TODO: {TaskStatus.IN_PROGRESS},
    TaskStatus.IN_PROGRESS: {TaskStatus.DONE},
    TaskStatus.DONE: set(),
}


def is_task_overdue(
    due_date: date | None,
    task_status: TaskStatus,
    today: date | None = None,
) -> bool:
    """
    Return True when a task is overdue.

    A task is overdue only when:
    - it has a due date,
    - the due date is before today,
    - its status is not Done.

    The optional today argument allows deterministic testing.
    """
    if due_date is None:
        return False

    if task_status == TaskStatus.DONE:
        return False

    comparison_date = today if today is not None else date.today()
    return due_date < comparison_date


def validate_status_transition(
    current_status: TaskStatus,
    new_status: TaskStatus,
) -> None:
    allowed_transitions = _ALLOWED_TRANSITIONS[current_status]

    if new_status not in allowed_transitions:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                f"Invalid status transition from "
                f"{current_status.value} to {new_status.value}"
            ),
        )