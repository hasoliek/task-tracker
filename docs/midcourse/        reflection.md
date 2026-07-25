# Reflection

## Project Experience

This project gave me practical experience extending an existing FastAPI application using an incremental development workflow. Rather than implementing all features at once, I completed the project in small, verifiable steps by updating the backend, adding automated tests, integrating the frontend, and validating each change before moving to the next task. This approach made debugging easier and reduced the risk of introducing regressions as new functionality was added.

## Working with AI

AI was a valuable development assistant throughout the project. I used it to generate implementation ideas, propose code changes, create test cases, and suggest frontend updates. However, I quickly learned that AI-generated code should always be reviewed rather than accepted automatically. Some responses were accepted because they met the requirements, while others required editing or were rejected completely.

One important example occurred when AI incorrectly inserted pytest test functions into `app/models.py` instead of the test file. This caused the application to fail because production code and test code had been mixed together. I rejected that response, restored the models file, rewrote the prompt to specify that only `tests/test_tasks.py` should be modified, and then verified the corrected implementation. This experience demonstrated the importance of carefully reviewing AI-generated output and writing precise prompts.

## Importance of Testing

Testing became one of the most valuable parts of my development workflow. After each significant change, I ran focused pytest tests, performed manual browser verification, or used API requests to confirm that the implementation behaved as expected. During development, one overdue-filter test failed because the API endpoint did not forward the new query parameter to the storage layer. The failing test immediately identified the missing implementation, allowing me to correct the issue before running the complete regression suite.

Reviewer feedback also helped strengthen the project by improving backend validation. I updated the application to reject explicit `null` values for required fields and to reject blank tags instead of silently removing them. After completing all corrections, the final regression suite reported **37 passing tests**, confirming that the new functionality had been added without breaking existing behavior.

## Lessons Learned

This project reinforced several software engineering practices. I learned that effective AI-assisted development depends on writing clear, specific prompts, verifying generated code through testing, and treating AI as a development assistant rather than an autonomous programmer. Combining careful prompt engineering with automated testing and manual verification allowed me to implement the required features while maintaining the stability of the existing application. I also gained additional experience working with FastAPI, Pydantic models, frontend integration, Git, and incremental debugging.