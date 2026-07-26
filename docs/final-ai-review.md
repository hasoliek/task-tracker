# Final AI Review and Ownership Evidence

## AGENTS.md Guardrails

- Repo-specific stack and commands included: **Yes**
- Docs-first/read-first guidance included: **Yes**
- Unexpected app/frontend edits rule included: **Yes**

---

## AI Code Review Mini Log

| AI Suggestion | Grade | My Evaluation | Outcome |
|--------------|-------|---------------|---------|
| Add Docker support with a non-root runtime user. | Useful | This improved deployment readiness and followed container security best practices. | Accepted and implemented. Verified using `docker exec id` showing `uid=10001(appuser)`. |
| Verify the application before updating documentation. | Useful | This prevented documentation from drifting away from the actual application behaviour. | Accepted. Backend, frontend and pytest were verified before finalizing the documentation. |
| Serve the frontend using an HTTP server instead of opening `index.html` directly. | Useful | This correctly identified the cause of the frontend communication issue because browser requests from `file://` were blocked. | Accepted. Frontend verified using `python -m http.server 5500`. |
| Re-run every completed verification after documentation-only edits. | Partially Useful | Once the application and tests had already been verified, repeating the same runtime checks after documentation-only edits did not provide additional confidence. | Not repeated after documentation-only changes. |

---

## AI Security Review

| AI Finding | Grade | My Evaluation | Outcome |
|-----------|-------|---------------|---------|
| Do not commit `.env` files. | Valid | This is standard security practice and was already enforced in the repository. | Confirmed through `.gitignore`. |
| Run Docker as a non-root user. | Valid | This strengthened container security without affecting functionality. | Implemented and verified. |
| Exclude unnecessary files from the Docker image. | Valid | Reduces image size and prevents accidental inclusion of development files. | Implemented through `.dockerignore`. |

---



## Independent Manual Security Review

After completing the implementation, I performed an independent review of the running application and repository without using the AI security review as a checklist. My objective was to identify issues through my own testing and inspection and verify that the application behaved as expected.

| Manual Check | Method | Finding |
|-------------|--------|---------|
| Error response handling | Accessed invalid API endpoints and requested resources that did not exist. | Verified that the application returned appropriate HTTP error responses with structured JSON messages and did not expose Python stack traces or internal implementation details. |
| Input validation | Submitted invalid task data, including incorrect field values and incomplete requests. | Confirmed that FastAPI rejected invalid requests with validation errors instead of accepting malformed input, demonstrating that request validation was functioning correctly. |
| Frontend network inspection | Used the browser Developer Tools (Network tab) while creating, updating, and deleting tasks. | Verified that the frontend communicated only with the expected backend API endpoints and observed no credentials or sensitive configuration values being transmitted in browser requests. |
| Repository inspection | Reviewed the repository contents, tracked files, and project configuration before submission. | Confirmed that the repository contained only the intended project source code, configuration files, and documentation, with no unintended or sensitive files identified during the review. |

---



## One AI Output I Corrected

Initially, I opened the frontend directly using:

```bash
open frontend/index.html
```

Although the backend API was working correctly, the frontend could not communicate with it because it was being loaded from `file://`.

After verifying the backend independently, I chose to serve the frontend using:

```bash
cd frontend
python -m http.server 5500
```

This resolved the communication issue without requiring any application code changes.

---

## Three AI Usage Rules

1. Never paste secrets, credentials or production information into AI tools.
2. Always verify AI-generated code by running tests and reviewing the implementation.
3. Accept AI suggestions only after confirming they are appropriate for this specific project.

---

## Ownership Statement

AI assisted me by suggesting implementation approaches, review steps, troubleshooting ideas, and documentation improvements, but I remained responsible for all technical decisions. I accepted some suggestions, adapted others to fit the project, and independently evaluated every recommendation before deciding whether to apply it. I personally verified the backend, frontend, automated tests, Docker configuration, CI pipeline, and documentation before submission. I understand the implementation and take full ownership of the final project.