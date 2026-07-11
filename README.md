# Task Tracker API

This is the Module 1 Task Tracker project for the AI-Assisted Coding course.

The current version contains a minimal FastAPI application with:

- A `GET /health` endpoint
- HTTP 200 response
- Current ISO timestamp
- Swagger documentation at `/docs`

CRUD endpoints are not included in Module 1.

## Setup

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it on macOS or Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the server:

```bash
uvicorn app.main:app --reload
```

## Test the health endpoint

```bash
curl http://127.0.0.1:8000/health
```

Expected response shape:

```json
{
  "status": "ok",
  "timestamp": "current ISO timestamp"
}
```

## Swagger documentation

Open:

```text
http://127.0.0.1:8000/docs
```