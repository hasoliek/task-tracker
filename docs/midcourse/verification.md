# Verification

## Project Setup

- Repository branch: `mid-course-project`
- All development was performed in the dedicated project branch before making any code changes.

## Baseline Verification

### Backend

- FastAPI application started successfully.
- `/health` endpoint returned HTTP 200.
- Swagger UI (`/docs`) loaded successfully.

### Frontend

- Kanban board loaded successfully.
- Create/Edit modal worked correctly.
- Drag-and-drop functionality worked.

### Existing Test Suite

Command:

```bash
python -m pytest -v

Result:

* 17 tests collected
* 17 tests passed
* 0 failures

# verifications for Feature 1 creation 

What was modified

Imported date from datetime.
Added due_date: Optional[date] = None to:
TaskCreate
TaskUpdate
TaskResponse
Why date instead of datetime or str

date enforces a date-only value (matches YYYY-MM-DD intent).
Avoids time/timezone ambiguity that comes with datetime.
Stronger validation and typing than raw str.
How optional preserves backward compatibility

Field defaults to None, so existing payloads without due_date remain valid.
Existing tasks and API clients are unaffected unless they choose to send/read due_date.
No existing validators, enums, or required fields were changed.

====================================== test session starts =======================================
platform darwin -- Python 3.14.0, pytest-9.1.1, pluggy-1.6.0 -- /Users/hassan/Documents/AI-Assisted-Coding/task-tracker/venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/hassan/Documents/AI-Assisted-Coding/task-tracker
plugins: anyio-4.14.1
collected 17 items                                                                               

tests/test_tasks.py::test_create_task_valid_returns_201_with_full_body PASSED              [  5%]
tests/test_tasks.py::test_create_task_missing_title_returns_422 PASSED                     [ 11%]
tests/test_tasks.py::test_create_task_blank_title_returns_422 PASSED                       [ 17%]
tests/test_tasks.py::test_create_task_invalid_priority_returns_422 PASSED                  [ 23%]
tests/test_tasks.py::test_create_task_unknown_field_returns_422 PASSED                     [ 29%]
tests/test_tasks.py::test_list_tasks_empty_returns_200_and_empty_list PASSED               [ 35%]
tests/test_tasks.py::test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list PASSED [ 41%]
tests/test_tasks.py::test_list_tasks_filter_by_priority_returns_only_matches PASSED        [ 47%]
tests/test_tasks.py::test_get_task_by_id_returns_task PASSED                               [ 52%]
tests/test_tasks.py::test_get_task_by_id_not_found_returns_404_with_detail PASSED          [ 58%]
tests/test_tasks.py::test_patch_partial_update_keeps_other_fields PASSED                   [ 64%]
tests/test_tasks.py::test_patch_not_found_returns_404 PASSED                               [ 70%]
tests/test_tasks.py::test_patch_valid_transition_todo_to_inprogress_returns_200 PASSED     [ 76%]
tests/test_tasks.py::test_patch_invalid_transition_todo_to_done_returns_422 PASSED         [ 82%]
tests/test_tasks.py::test_patch_same_status_returns_422 PASSED                             [ 88%]
tests/test_tasks.py::test_delete_existing_returns_204_no_body PASSED                       [ 94%]
tests/test_tasks.py::test_delete_missing_returns_404 PASSED                                [100%]

======================================== warnings summary ========================================
venv/lib/python3.14/site-packages/fastapi/testclient.py:1
  /Users/hassan/Documents/AI-Assisted-Coding/task-tracker/venv/lib/python3.14/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

tests/test_tasks.py::test_patch_invalid_transition_todo_to_done_returns_422
tests/test_tasks.py::test_patch_same_status_returns_422
  /Users/hassan/Documents/AI-Assisted-Coding/task-tracker/app/main.py:93: StarletteDeprecationWarning: 'HTTP_422_UNPROCESSABLE_ENTITY' is deprecated. Use 'HTTP_422_UNPROCESSABLE_CONTENT' instead.
    validate_status_transition(current_task.status, payload.status)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================= 17 passed, 3 warnings in 0.05s =================================

## Feature 1 – Model Layer Verification

### File Changed

- `app/models.py`

### Syntax Check

Command:

```bash
python -m compileall app

# 5.1 Prompt 2 Business Rules 

What was added

A reusable function is_task_overdue(due_date, status, today=None) using Python date.
Why optional today is useful

It allows deterministic tests by injecting a fixed date instead of relying on system clock.
How non-overdue cases are handled

due_date is None → returns False.
due_date == today (or current date) → returns False because only < today is overdue.
status == "Done" → returns False even if due date is in the past.

(venv) (base) hassan@Hassans-MacBook-Pro task-tracker % python -m compileall app
Listing 'app'...
(venv) (base) hassan@Hassans-MacBook-Pro task-tracker % python -m pytest -v
====================================== test session starts =======================================
platform darwin -- Python 3.14.0, pytest-9.1.1, pluggy-1.6.0 -- /Users/hassan/Documents/AI-Assisted-Coding/task-tracker/venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/hassan/Documents/AI-Assisted-Coding/task-tracker
plugins: anyio-4.14.1
collected 17 items                                                                               
# Feature 1, Business Rules update verification 

tests/test_tasks.py::test_create_task_valid_returns_201_with_full_body PASSED              [  5%]
tests/test_tasks.py::test_create_task_missing_title_returns_422 PASSED                     [ 11%]
tests/test_tasks.py::test_create_task_blank_title_returns_422 PASSED                       [ 17%]
tests/test_tasks.py::test_create_task_invalid_priority_returns_422 PASSED                  [ 23%]
tests/test_tasks.py::test_create_task_unknown_field_returns_422 PASSED                     [ 29%]
tests/test_tasks.py::test_list_tasks_empty_returns_200_and_empty_list PASSED               [ 35%]
tests/test_tasks.py::test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list PASSED [ 41%]
tests/test_tasks.py::test_list_tasks_filter_by_priority_returns_only_matches PASSED        [ 47%]
tests/test_tasks.py::test_get_task_by_id_returns_task PASSED                               [ 52%]
tests/test_tasks.py::test_get_task_by_id_not_found_returns_404_with_detail PASSED          [ 58%]
tests/test_tasks.py::test_patch_partial_update_keeps_other_fields PASSED                   [ 64%]
tests/test_tasks.py::test_patch_not_found_returns_404 PASSED                               [ 70%]
tests/test_tasks.py::test_patch_valid_transition_todo_to_inprogress_returns_200 PASSED     [ 76%]
tests/test_tasks.py::test_patch_invalid_transition_todo_to_done_returns_422 PASSED         [ 82%]
tests/test_tasks.py::test_patch_same_status_returns_422 PASSED                             [ 88%]
tests/test_tasks.py::test_delete_existing_returns_204_no_body PASSED                       [ 94%]
tests/test_tasks.py::test_delete_missing_returns_404 PASSED                                [100%]

======================================== warnings summary ========================================
venv/lib/python3.14/site-packages/fastapi/testclient.py:1
  /Users/hassan/Documents/AI-Assisted-Coding/task-tracker/venv/lib/python3.14/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

tests/test_tasks.py::test_patch_invalid_transition_todo_to_done_returns_422
tests/test_tasks.py::test_patch_same_status_returns_422
  /Users/hassan/Documents/AI-Assisted-Coding/task-tracker/app/main.py:93: StarletteDeprecationWarning: 'HTTP_422_UNPROCESSABLE_ENTITY' is deprecated. Use 'HTTP_422_UNPROCESSABLE_CONTENT' instead.
    validate_status_transition(current_task.status, payload.status)

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
================================= 17 passed, 3 warnings in 0.03s =================================

## Feature 1 Final Verification — Due Dates and Overdue Filtering

### Scope verified

The following backend changes were verified:

- `TaskCreate` accepts an optional `due_date`.
- `TaskUpdate` accepts an optional `due_date`.
- `TaskResponse` returns `due_date`.
- Requests without a due date remain valid.
- Due dates use the `YYYY-MM-DD` format through Python's `date` type.
- New tasks persist the due date.
- Partial updates preserve unchanged fields.
- The overdue calculation is centralized in `is_task_overdue`.
- A task is overdue only when:
  - its due date is before today,
  - it is not marked `Done`.
- Existing status and priority filters remain functional.
- The storage reset helper remains available for isolated tests.
- Existing CRUD and status-transition behavior remains intact.

### Commands executed

```bash
python -m compileall app
python -m pytest -v


