# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Tech Stack

- **Python** — Project/course target: **Python 3.11**. Current local environment appears to use Python 3.13/3.14 [VERIFY] (README says "Python 3.13 or later"; bytecode cache is cpython-313/314). There are no version pins in `requirements.txt`.
- **FastAPI** — REST API framework
- **Pydantic v2** — request/response models and validation (uses `field_validator`, `ConfigDict`, `model_copy` — Pydantic v2 APIs)
- **Uvicorn** — ASGI server
- **pytest** — test runner
- **httpx** — HTTP client (used by FastAPI's `TestClient` in tests)
- **Vanilla JavaScript frontend** — single static `frontend/index.html` (inline CSS/JS, no framework, no build step)

Dependencies are unpinned in `requirements.txt`: `fastapi`, `uvicorn`, `pydantic`, `pytest`, `httpx`.

## Exact Run Command

```bash
uvicorn app.main:app --reload --port 8000
```

Runs from the project root with the venv activated (`source venv/bin/activate`). API at http://127.0.0.1:8000, interactive docs at `/docs`.

## Exact Test Command

```bash
pytest -v
```

Single test example:

```bash
pytest -v tests/test_tasks.py::test_create_task_valid_returns_201_with_full_body
```

`tests/verify_a.py` is a standalone model-validation script (run with `python tests/verify_a.py`) that prints PASS/FAIL — it is not collected by pytest.

## Architecture Summary

FastAPI backend + a single static-HTML Kanban frontend. The backend is three layers, one direction only: `main.py` (routes) → `storage.py` (persistence) → `business_rules.py` / `models.py`.

**Backend files (`app/`)**

- `main.py` — route handlers only. Owns HTTP concerns: 404s for missing tasks, and calling `validate_status_transition` before any status change on PATCH. Endpoints: `GET /health`, `POST /tasks`, `GET /tasks` (with `status`/`priority`/`overdue`/`tag` query filters), `GET /tasks/{id}`, `PATCH /tasks/{id}`, `DELETE /tasks/{id}`.
- `storage.py` — persistence and list filtering (`get_all_tasks`).
- `business_rules.py` — pure domain logic (status transitions, overdue calculation); no storage access.
- `models.py` — Pydantic schemas (`TaskCreate`, `TaskUpdate`, `TaskResponse`, `TaskStatus`, `TaskPriority`).

**Frontend files**

- `frontend/index.html` — single self-contained file (inline CSS/JS). Backend base URL is **hardcoded** as `API_BASE_URL = "http://127.0.0.1:8000"`.

**Tests (`tests/`)**

- `conftest.py` — fixtures (`client`, `created_task`) and an autouse `_reset_storage` fixture that clears the in-memory store before and after every test, so tests are isolated.
- `test_tasks.py` — API tests via FastAPI `TestClient`.
- `verify_a.py` — standalone validation script (see Exact Test Command).

**Where task rules live** — `app/business_rules.py` (status-transition table and overdue calculation) and `app/models.py` (title/tag validation). Route-level enforcement of transitions happens in `app/main.py`.

**Storage approach** — in-memory only: a module-level dict `_tasks` in `storage.py`. There is no database. All data is lost on restart and it is not concurrency-safe. `storage._reset()` clears it and exists for tests.

**Documentation** — project docs (user stories, mini-ADR, prompt log, verification, reflection) live in `docs/midcourse/`. The submission branch is `mid-course-project`.

## Business Rules

**Task status values** (`TaskStatus` in `models.py`): `ToDo`, `InProgress`, `Done`.

**Priority values** (`TaskPriority`): `Low`, `Medium`, `High` (default `Medium`).

**Allowed status transitions** (`_ALLOWED_TRANSITIONS` in `business_rules.py`, enforced in the PATCH handler) — linear and irreversible:

- `ToDo → InProgress`
- `InProgress → Done`
- `Done →` (nothing; terminal)

Any other transition (including skipping a state or moving backward) is rejected with **HTTP 422**.

**Due date and overdue** — `due_date` is optional. Overdue is **computed on demand** by `is_task_overdue` purely for **server-side filtering** — it is never stored and the API response does **not** include an `overdue` field. A task counts as overdue only when it has a `due_date` in the past *and* its status is not `Done`. `is_task_overdue` accepts an optional `today` argument for deterministic tests. Overdue is exposed only as the `GET /tasks?overdue=true` filter. Verified by `test_list_tasks_overdue_true_returns_only_overdue_tasks` and `test_done_task_with_past_due_date_is_not_overdue` in `tests/test_tasks.py`, which assert on the filtered list, not on any response field.

**Tags** — implemented. Multiple tags per task (`tags: list[str]`, default empty). On create/update, tags are validated and cleaned by `validate_and_clean_tags`: each tag is stripped, blank tags raise a `ValueError`, and duplicates are de-duped (order preserved). Tasks can be filtered by a single tag via `GET /tasks?tag=<tag>`.

**Field validation** — models use `extra="forbid"`, so unknown fields are rejected. `title` is stripped and must be 1–200 chars (blank titles raise).

## UI States and CORS

**UI states** (`frontend/index.html`) — the board renders explicit `loading`, `empty`, and `error` states. The empty state message adapts to the overdue filter ("No overdue tasks found." vs "No tasks found."). There is an "Overdue only" filter checkbox, an overdue badge on cards, and inline form-error display for the create form.

**Known frontend/API mismatch** — the frontend renders the overdue badge from `task.overdue === true` (`frontend/index.html`, ~line 838), but the API response has no `overdue` field (see Business Rules), so `task.overdue` is always `undefined` and the badge never renders from API data. Documented as-is; do not change application code to "fix" it in this repository without being asked.

**CORS** (`main.py`) — the API only allows origins on **port 5500**: `http://127.0.0.1:5500` and `http://localhost:5500`. Serve the frontend on port 5500 (`python -m http.server 5500` from `frontend/`, or VS Code Live Server) or API calls will be blocked. Note the split: the frontend is served on 5500 but calls the backend hardcoded on 8000 (allowed by the CORS config above).

## Do-Not Rules

- **Do not add authentication.**
- **Do not add a database** — storage is intentionally the in-memory `_tasks` dict.
- **Do not add deployment steps** (Docker, CI/CD, hosting config, etc.).
- **Do not make major UI changes without asking first.**
