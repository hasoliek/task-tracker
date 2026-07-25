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

Workflow file:

```
.github/workflows/ci.yml
```

After pushing the `final-project` branch, I verified the workflow from the GitHub Actions page.

Observed result:

- Workflow: **CI**
- Job: **test**
- Trigger: **Push**
- Status: **Passed** ✅
- Python version: **3.11**
- Test command executed:

```bash
pytest -v
```

Evidence:

The latest GitHub Actions workflow completed successfully, confirming that the repository builds correctly and all automated tests pass.

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

| Claim | Evidence Collected | Result |
|-------|--------------------|--------|
| Backend runs using `uvicorn app.main:app --reload --port 8000`. | Started the backend with `uvicorn app.main:app --reload --port 8000`, then ran `curl http://127.0.0.1:8000/health` and received `HTTP/1.1 200 OK` with `{"status":"ok"}`. | Verified |
| Frontend communicates with the backend. | Served the frontend using `python -m http.server 5500`, opened `http://127.0.0.1:5500`, created a task, and confirmed it appeared on the Kanban board and could be edited successfully. | Verified |
| Local test suite passes. | Executed `pytest` and obtained `37 passed, 3 warnings in 0.07s`. The warnings were dependency deprecation warnings only and did not affect application functionality. | Verified |
| CI executes automated tests. | Checked the latest GitHub Actions **CI** workflow after pushing the `final-project` branch. The **test** job completed successfully using Python 3.11 and `pytest -v`. | Verified |
| Docker image runs successfully. | Built the image using `docker build -t task-tracker-final .`, started it using `docker run --rm -d --name task-tracker-final -p 8001:8000 task-tracker-final`, then verified `curl http://127.0.0.1:8001/health` returned `HTTP/1.1 200 OK`. | Verified |
