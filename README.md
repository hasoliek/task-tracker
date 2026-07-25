# Task Tracker API

## Overview

This project was completed as the **Mid-Course Project** for the **AI-Assisted Coding** course.

The application is a FastAPI-based Task Tracker with a Kanban-style frontend. It provides a REST API together with a browser-based interface for creating, updating, organizing, and managing tasks.

> **Submission branch:** `mid-course-project`

---

# Implemented Features

## Core Features

- Create tasks
- Retrieve tasks
- Update tasks
- Delete tasks
- Drag-and-drop status updates
- Status transition validation
- Priority filtering

## Feature 1 – Due Dates and Overdue Filtering

- Optional due dates
- Automatic overdue calculation
- Overdue task filtering
- Due date display on task cards
- Overdue indicator for active overdue tasks

## Feature 2 – Tags and Tag Filtering

- Multiple tags per task
- Tag validation
- Tag display on task cards
- Tag-based filtering

---

# Project Structure

```text
app/
frontend/
tests/
docs/
```

---

# Requirements

- Python 3.11 (project/course target; also used by CI)
- Virtual environment
- FastAPI
- Uvicorn

---

# Installation

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it (macOS/Linux):

```bash
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

# Running the Backend

Start the FastAPI server from the project root:

```bash
uvicorn app.main:app --reload --port 8000
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Running the Frontend

The frontend is contained in:

```text
frontend/index.html
```

### Recommended

Open `frontend/index.html` using **VS Code Live Server** while the FastAPI backend is running.

### Alternative

From the `frontend` directory:

```bash
python -m http.server 5500
```

Then open:

```text
http://127.0.0.1:5500
```

The frontend communicates with the FastAPI backend running on:

```text
http://127.0.0.1:8000
```

---

# Running the Tests

From the project root, execute:

```bash
pytest -v
```

All tests in `tests/` should pass. Any warnings shown are dependency/deprecation warnings and do not affect application functionality.

> **Contributor note:** Make sure the tests pass locally before pushing — CI runs `pytest -v` automatically on every push and pull request (see [Continuous Integration](#continuous-integration)).

---

# Continuous Integration

Automated testing runs via GitHub Actions.

- **Workflow file:** `.github/workflows/ci.yml`
- **Triggers:** every `push` and `pull_request`
- **Python version:** 3.11
- **Steps:** installs dependencies from `requirements.txt`, then runs `pytest -v`

The build fails if any test fails.

---

# Documentation

Project documentation is located in:

```text
docs/midcourse/
```

The folder includes:

- User Stories
- Mini ADR
- AI Prompt Log
- Verification Log
- Reflection

---

# Technologies Used

- FastAPI
- Pydantic
- Pytest
- HTML
- CSS
- JavaScript
- Git

---

# AI-Assisted Development

AI was used throughout the project to assist with:

- implementation planning,
- code generation,
- test generation,
- debugging,
- frontend integration,
- documentation.

All AI-generated output was manually reviewed, tested, and either accepted, edited, or rejected before being incorporated into the final solution.

Verification included automated regression testing, manual browser testing, deliberate break tests, and API validation to ensure that new features did not introduce regressions.

---

# Final Project

**Branch reviewed:** `final-project`

## What this submission demonstrates

- The existing Task Tracker application remains within the intended course scope with no unrelated product features added.
- The backend runs successfully and the `/health` endpoint returns **HTTP 200 OK**.
- The complete test suite passes successfully (`37 passed`).
- GitHub Actions runs the pytest suite on every push and pull request.
- A Docker image can be built and run successfully, with `/health` verified from inside the container.
- AI review, security verification, and ownership evidence are documented in the `docs/` folder.

---

## How to run locally

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Start the backend:

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Serve the frontend:

```bash
cd frontend
python -m http.server 5500
```

Open:

```text
http://127.0.0.1:5500
```

---

## How to run tests

```bash
pytest
```

Current baseline:

```text
37 passed, 3 warnings
```

---

## How to run with Docker

Build the image:

```bash
docker build -t task-tracker-final .
```

Run the container:

```bash
docker run --rm -d \
  --name task-tracker-final \
  -p 8001:8000 \
  task-tracker-final
```

Verify:

```bash
curl http://127.0.0.1:8001/health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

## Evidence files

- `docs/release-evidence.md`
- `docs/final-ai-review.md`
- `docs/ai-playbook.md`

---

## AI assistance summary

AI was used to assist with:

- implementation planning
- debugging
- automated test review
- CI workflow review
- Docker configuration
- documentation drafting
- release verification

All AI-generated suggestions were manually reviewed before acceptance.

Verification included:

- running the complete pytest suite
- manual frontend verification
- backend `/health` verification
- Docker runtime verification
- code and documentation review

One AI suggestion was corrected during the project by serving the frontend through an HTTP server instead of opening `index.html` directly, ensuring proper backend communication before documenting the release evidence.

