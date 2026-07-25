# Release Evidence

## Baseline

- Branch: `final-project`
- Date: `2026-07-25`

### Local app run command

```bash
uvicorn app.main:app --reload --port 8000
```

### Backend health verification

```text
HTTP/1.1 200 OK
{"status":"ok","timestamp":"2026-07-25T12:23:58.874668+00:00"}
```

### Frontend verification

Frontend served using:

```bash
cd frontend
python -m http.server 5500
```

Manual verification completed:

- Kanban board loaded successfully.
- Backend communication verified.
- Empty task state displayed correctly.
- New Task dialog opened successfully.
- Test task created successfully.
- Edit Task dialog opened successfully.

### Test verification

Command:

```bash
pytest
```

Result:

```text
37 passed, 3 warnings in 0.07s
```

The warnings are dependency deprecation warnings only and do not affect application functionality.

---

## CI Evidence

- Workflow file: `.github/workflows/ci.yml`
- Triggered on `push` and `pull_request`
- Python version: `3.11`
- Dependencies installed from `requirements.txt`
- Test command:

```bash
pytest -v
```

Shortcut verification:

- No `continue-on-error`
- No `|| true`
- Tests are not skipped
- Explicit Python version configured

GitHub Actions run will be recorded after the final push.

---

## Docker Evidence

Build command:

```bash
docker build -t task-tracker-final .
```

Run command:

```bash
docker run --rm -d \
  --name task-tracker-final \
  -p 8001:8000 \
  task-tracker-final
```

Health verification:

```text
HTTP/1.1 200 OK
{"status":"ok","timestamp":"2026-07-25T12:47:36.761762+00:00"}
```

Container user:

```text
uid=10001(appuser)
```

Docker safety verification:

- Non-root user configured.
- `.env` excluded.
- `.env.*` excluded.
- Git metadata excluded.
- Virtual environment excluded.
- Tests excluded.
- Documentation excluded.
- Frontend excluded.

---

## Documentation Claim vs Reality

| Claim | Evidence | Result |
|-------|----------|--------|
| Backend runs using `uvicorn app.main:app --reload --port 8000`. | Manual verification and `/health`. | Confirmed |
| Frontend communicates with backend. | Manual browser verification. | Confirmed |
| CI runs pytest. | `.github/workflows/ci.yml` | Confirmed |
| Local test suite passes. | `pytest` execution. | Confirmed |
| Docker image runs successfully. | Local Docker build and `/health` verification. | Confirmed |
