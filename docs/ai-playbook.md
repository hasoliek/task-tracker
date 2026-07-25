# AI Playbook

## When I Reach for AI First

I use AI early when I need help understanding a problem, exploring implementation options, or generating a starting point for documentation or code. During this project, AI was most helpful for:

- Explaining Docker configuration and container best practices.
- Reviewing documentation for completeness and consistency.
- Suggesting improvements to the FastAPI project structure.
- Troubleshooting frontend communication issues.
- Reviewing release readiness before submission.

I prefer asking focused questions about one problem at a time rather than requesting large code rewrites.

---

## When I Do Not Reach for AI First

I avoid using AI when the answer should come directly from my own verification or from the project itself. Instead, I first:

- Run the application locally.
- Execute the full pytest suite.
- Inspect repository files such as `.gitignore`, `.dockerignore`, and the Dockerfile.
- Verify API responses manually.
- Review Git changes before committing.

I rely on direct testing rather than assuming AI-generated answers are correct.

---

## My Non-Negotiables

Regardless of AI recommendations, I always:

- Review every suggested change before applying it.
- Run automated tests after code changes.
- Perform manual verification of important functionality.
- Never commit secrets or sensitive information.
- Ensure documentation reflects the actual implementation rather than assumptions.

---

## My Review Rules

Before accepting any AI-generated suggestion, I ask myself:

1. Does it solve the actual problem?
2. Can I explain how it works?
3. Have I verified it by testing or inspection?
4. Does it follow the project requirements?
5. Does it introduce unnecessary complexity?

Only after answering these questions do I include the change in the project.

---

## What I Am Still Figuring Out

During this project I became more confident using AI as a development assistant, but I still want to improve at:

- Writing better prompts for complex technical problems.
- Identifying unnecessary AI suggestions more quickly.
- Improving Docker and CI/CD knowledge.
- Designing larger projects with less dependence on AI guidance.

---

## Decision Card

| Situation | My Decision |
|-----------|-------------|
| Understanding a new concept | Ask AI for an explanation first. |
| Writing new code | Use AI for ideas, then review and modify the solution myself. |
| Debugging failures | Verify logs, tests, and application behaviour before accepting AI conclusions. |
| Security-related changes | Perform my own manual verification before accepting AI recommendations. |
| Final submission | Personally verify the application, tests, Docker configuration, CI results, and documentation before submitting. |