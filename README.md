# Task Tracker API

## Overview

This project was completed as the **Mid-Course Project** for the AI-Assisted Coding course.

The application is a FastAPI-based Task Tracker with a Kanban-style frontend. It supports task management through a REST API and a browser-based interface.

### Implemented Features

#### Core Features

- Create tasks
- Retrieve tasks
- Update tasks
- Delete tasks
- Drag-and-drop status updates
- Status transition validation
- Priority filtering

#### Feature 1 – Due Dates and Overdue Filtering

- Optional due dates
- Automatic overdue calculation
- Overdue task filtering
- Due date display on task cards

#### Feature 2 – Tags and Tag Filtering

- Multiple tags per task
- Tag validation
- Tag display on task cards
- Tag-based filtering

---

# Project Structure

```
app/
frontend/
tests/
docs/
```

---

# Requirements

- Python 3.13+
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

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Run the Backend

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The backend will be available at:

```
http://127.0.0.1:8000
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

---

# Run the Frontend

From the project directory:

```bash
cd frontend
python -m http.server 5500
```

Open:

```
http://127.0.0.1:5500
```

The frontend communicates with the FastAPI backend running on port 8000.

---

# Running Tests

Run the complete regression suite:

```bash
pytest
```

Expected result:

```
31 passed
```

(Deprecation warnings may appear depending on installed package versions.)

---

# Documentation

Project documentation is available under:

```
docs/midcourse/
```

Including:

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

AI was used to assist with:

- implementation planning,
- code generation,
- test generation,
- debugging,
- frontend integration,
- documentation.

All AI-generated outputs were manually reviewed, tested, and corrected before acceptance.