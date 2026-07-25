# AGENTS.md

## Project Overview

This repository contains the final project submission for the AI-Assisted Coding course.

The application is a FastAPI-based Task Tracker with a Kanban frontend.

The purpose of this document is to provide guidance for future AI assistants and human contributors working on this repository.

---

## Project Goals

When modifying this project:

- Preserve existing API behavior unless intentionally changing requirements.
- Keep all existing tests passing.
- Prefer small, incremental changes.
- Maintain compatibility with the frontend.
- Preserve backward compatibility for the REST API whenever possible.

---

## Development Workflow

Before making changes:

1. Read the README.
2. Review existing tests.
3. Understand the current implementation.
4. Make the smallest possible change.
5. Update or add tests if behavior changes.
6. Run the complete pytest suite.

---

## Coding Standards

- Follow existing project structure.
- Use descriptive names.
- Keep functions focused.
- Avoid unnecessary complexity.
- Reuse existing business rules where possible.

---

## Verification Checklist

Before submitting changes:

- Backend starts successfully.
- `/health` returns HTTP 200.
- All pytest tests pass.
- Frontend loads correctly.
- Docker image builds successfully.
- Container runs as non-root.

---

## AI Usage

AI-generated suggestions should never be accepted automatically.

Every recommendation should be:

- reviewed,
- tested,
- validated,

before being committed.

Human review is the final authority for all repository changes.
