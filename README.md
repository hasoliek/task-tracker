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