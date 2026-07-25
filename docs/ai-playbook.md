# AI Playbook

## Purpose

This document summarizes the practical workflow followed while completing the final project using AI assistance.

---

## Workflow

1. Understand the assignment requirements before making changes.
2. Verify the existing application by running the backend, frontend, and automated tests.
3. Ask AI for small, focused changes instead of large rewrites.
4. Review every AI suggestion before applying it.
5. Test every accepted change locally.
6. Record important AI-assisted decisions in the project documentation.
7. Perform a final verification before committing.

---

## Effective Prompting Practices

The following approaches produced the most reliable AI assistance:

- Provide the current project context before asking for code.
- Request incremental changes instead of complete rewrites.
- Ask AI to explain the reasoning behind recommendations.
- Verify outputs using automated tests.
- Use manual testing to confirm frontend behavior.

---

## Verification Process

Every accepted AI recommendation was verified using one or more of the following:

- Pytest test suite
- Backend `/health` endpoint
- Manual browser testing
- Docker build and runtime verification
- Git diff review before committing

---

## Lessons Learned

- AI is most effective when given clear project context.
- Small iterative prompts reduce mistakes.
- Automated tests are essential for validating AI-generated code.
- Human review remains necessary before accepting any change.
- Documentation should be updated alongside implementation changes.

---

## Future Improvements

If this project continues, AI can assist with:

- Increasing test coverage
- API documentation improvements
- Performance optimization
- Additional frontend enhancements
- Refactoring while preserving existing behavior
