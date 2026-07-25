# Final AI Review and Ownership Evidence

## AGENTS.md Guardrails

- Repo-specific stack and commands included: **Yes**
- Docs-first/read-first guidance included: **Yes**
- Unexpected app/frontend edits rule included: **Yes**

---

## AI Code Review Mini Log

| AI Comment | Grade | Reason | Verification |
|------------|-------|--------|--------------|
| Add Docker support with a non-root runtime user. | Useful | Improved release readiness and container security. | Implemented and verified using `docker exec id`. |
| Verify the existing application before making documentation changes. | Useful | Prevented documenting unverified functionality. | Backend, frontend and pytest verified before documentation. |
| Serve the frontend using an HTTP server instead of opening `index.html` directly. | Useful | Solved the frontend communication issue caused by using `file://`. | Verified by loading the Kanban board successfully. |

---

## AI Security Mini Review

| Finding | File Evidence | Grade | Reason | Action |
|---------|---------------|-------|--------|--------|
| `.env` should never be committed. | `.gitignore` | Valid | `.env` is ignored and not tracked. | No action required. |
| Run the Docker container as a non-root user. | `Dockerfile` | Valid | Container now runs as `appuser`. | Implemented. |
| Exclude virtual environments, Git metadata and caches from Docker images. | `.dockerignore` | Valid | Reduces image size and prevents accidental disclosure. | Implemented. |

---

## Manual Security Check

I manually verified that:

- `.env` is ignored by Git.
- Docker runs as a non-root user.
- The backend `/health` endpoint returns HTTP 200.
- The complete pytest suite passes.
- No credentials or secrets are committed in the repository.

---

## One AI Output I Corrected

Initially the frontend was opened directly using `open frontend/index.html`. Although the backend was functioning correctly, the frontend reported **Load failed** because it was not being served over HTTP.

Instead of assuming the backend was broken, I verified the API manually and then served the frontend using:

```bash
cd frontend
python -m http.server 5500
```

This corrected the issue without modifying the application code.

---

## Three AI Usage Rules

1. Never paste secrets, credentials or production information into AI tools.
2. Always verify AI-generated code by running tests and reviewing the implementation.
3. Record significant AI contributions and manually verify important changes before committing.

---

## Ownership Statement

I used AI as a development assistant rather than an automatic code generator. Every significant recommendation was reviewed, tested and verified before being accepted. I personally validated the backend, frontend, automated tests, CI configuration and Docker runtime. I understand every change included in this repository and I am comfortable submitting it as my own work.
