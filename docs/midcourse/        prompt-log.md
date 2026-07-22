# Prompt 1 – Generate the User Stories (Feature 1)
Generate user stories for the Mid-Course Task Tracker Feature 1: Due Dates + Overdue Filter in the same format and quality as the Module 1 user stories.

Example:

Story:
As a team member, I want to create a task so that I can track work that needs to be completed.

Acceptance Criteria:
- A task can be created with a title, description, status, priority, and assignee.
- The title is required; missing or blank title returns HTTP 422.
- The newly created task appears in the task list with the assigned values.

Now generate four user stories for the Due Dates + Overdue Filter feature.

Constraints:
- Use "team member" as the user role.
- Focus only on the Due Dates + Overdue Filter feature.
- Include user stories covering:
  • creating a task with an optional due date,
  • updating or removing a due date,
  • automatic overdue detection,
  • filtering overdue tasks.
- Every story must include acceptance criteria.
- Include at least one failure case.
- Do not mention authentication, login, user accounts, notifications, mobile apps, databases, or features outside the project scope.
- Keep the scope suitable for the existing FastAPI Task Tracker.

Output format:
Return each story using only the headings:

Story
Acceptance Criteria

# Prompt 2 – Generate the User Stories (Feature 2)
Generate user stories for the Mid-Course Task Tracker Feature 2: Tags / Labels in the same format and quality as the Module 1 user stories.

Example:

Story:
As a team member, I want to create a task so that I can track work that needs to be completed.

Acceptance Criteria:
- A task can be created with a title, description, status, priority, and assignee.
- The title is required; missing or blank title returns HTTP 422.
- The newly created task appears in the task list with the assigned values.

Now generate four user stories for the Tags / Labels feature.

Constraints:
- Use "team member" as the user role.
- Focus only on the Tags / Labels feature.
- Include user stories covering:
  • adding tags,
  • updating tags,
  • displaying tags,
  • filtering tasks by tag.
- Every story must include acceptance criteria.
- Include at least one failure case.
- Do not mention authentication, login, user accounts, notifications, mobile apps, databases, or features outside the project scope.
- Keep the scope suitable for the existing FastAPI Task Tracker.

Output format:
Return each story using only the headings:

Story
Acceptance Criteria

# Prompt 3 – Convert the Generated Stories into the Documentation Table

Using the generated user stories for this feature, convert them into a Markdown table matching the same style used in Module 1.

The table must contain the following columns:

| ID | Story | Acceptance Criteria | Notes / Assumptions |

Requirements:
- Number the stories sequentially (US-1, US-2, ...).
- Keep the story text concise.
- Convert the acceptance criteria into bullet points inside the table cell.
- Add a short Notes / Assumptions column describing any assumptions made for that story.
- Maintain a professional documentation style suitable for project submission.
- Do not change the meaning of the user stories.

I reviewed the generated user stories for Feature 1 (Due Dates + Overdue Filter) and I do not agree with one of the AI assumptions.

The AI assumed that overdue status should be stored as part of each task.

# Prompt 4 – Correct AI Assumption (Feature 1)

I believe this is not the best design because overdue status changes automatically as time passes and should not be stored permanently.

Please revise the user stories and assumptions so that overdue status is calculated dynamically from the task's due date, the current date, and the task status.

Explain why this design is preferable and update only the affected assumption without changing the scope of the feature.

# Prompt 5 – Correct AI Assumption (Feature 2)
I reviewed the generated user stories for Feature 2 (Tags / Labels) and I do not agree with one of the AI assumptions.

The AI assumed that tags could be stored as a single comma-separated string.

I believe this approach makes validation, updating, and filtering more difficult.

Please revise the user stories and assumptions so that tags are represented as a list of strings instead.

Explain why this design is preferable and update only the affected assumption without changing the scope of the feature.

# Phase 5.1 – Prompt 1: models change update

I have an existing FastAPI Task Tracker application, and I am implementing Feature 1: Due Dates and Overdue Filter.

Please update only the file `app/models.py`.

Requirements:
- Add an optional `due_date` field to the existing `TaskCreate`, `TaskUpdate`, and `TaskResponse` models.
- Use Python's `date` type from the `datetime` module.
- The field should default to `None`.
- Preserve all existing validation, enums, field definitions, and model behavior.
- Do not modify any unrelated models or business logic.
- Keep the implementation fully backward compatible with the existing application.
- Do not make changes to any other files.

After making the changes, explain:
1. What was modified.
2. Why the `date` type was chosen instead of `datetime` or `str`.
3. How the optional field preserves backward compatibility.

## Feature 1 – Prompt 2: Implement Overdue Business Rule

### Prompt

I asked the AI to update only `app/business_rules.py` by adding a reusable helper function to determine whether a task is overdue while preserving the existing status-transition logic.

### AI Response Summary

The AI added a reusable `is_task_overdue()` function that:

- Accepts an optional due date.
- Accepts the task status.
- Accepts an optional `today` parameter for deterministic testing.
- Returns `True` only when:
  - the task has a due date,
  - the due date is before the current date,
  - the task status is not `Done`.

The AI also explained that:

- The optional `today` parameter allows tests to use a fixed date instead of depending on the system clock.
- Tasks without a due date are not overdue.
- Tasks due today are not overdue.
- Completed tasks are never overdue, even if their due date has passed.

### Human Review

I reviewed the proposed implementation before accepting it. I agreed with introducing a reusable helper function because it centralizes the overdue business rule and avoids duplicating logic throughout the application. I also accepted the optional `today` parameter because it supports deterministic and repeatable unit testing.

# 5.1 prompt 3 - storage update

I am continuing Feature 1 (Due Dates and Overdue Filter) in my existing FastAPI Task Tracker.

Please update only `app/storage.py`.

Requirements:

- Extend the existing task listing functionality to support an optional `overdue` filter.
- Reuse the existing `is_task_overdue()` helper from `business_rules.py`.
- Do not duplicate overdue calculation logic.
- Preserve the existing status and priority filtering behavior.
- If `overdue` is not provided, the existing behavior should remain unchanged.
- If `overdue=True`, return only overdue tasks.
- If `overdue=False`, return only tasks that are not overdue.
- Do not modify task creation, retrieval, update, or deletion logic.
- Do not modify any other files.

After making the changes, explain:

1. What was modified.
2. How the existing filtering behavior was preserved.
3. Why reusing the business rule is preferable to duplicating the overdue logic.

# prompt 3 result correction 

Your previous response stated that app/storage.py had been updated, but the actual file still contains none of those changes.

Please correct only app/storage.py.

Required changes:
1. Import is_task_overdue from app.business_rules.
2. In add_task(), include due_date=payload.due_date when constructing TaskResponse.
3. Extend get_all_tasks() with an optional overdue: Optional[bool] = None parameter.
4. Preserve the existing status and priority filters.
5. When overdue is not None, filter tasks by calling:
   is_task_overdue(task.due_date, task.status)
6. Do not duplicate overdue comparison logic.
7. Do not modify update, delete, retrieval, or reset behavior.
8. Do not modify any other file.

After editing, show the exact diff rather than only summarizing the intended changes.

# prompt 3 result correction2 

The test suite currently fails with:

ImportError: cannot import name 'is_task_overdue' from 'app.business_rules'

Your previous response claimed that the function had been added, but the actual file does not contain it.

Please update only app/business_rules.py.

Requirements:
- Import date from datetime.
- Add a reusable function named is_task_overdue.
- Parameters:
  - due_date: date | None
  - task_status: TaskStatus
  - today: date | None = None
- Return False when due_date is None.
- Return False when task_status is TaskStatus.DONE.
- Return False when due_date is today.
- Return True only when due_date is earlier than today and the task is not Done.
- Use today or date.today() as the comparison date.
- Preserve all existing status-transition logic exactly.
- Do not modify any other file.
- Show the exact diff after editing.

## Feature 1 — Due Dates and Overdue Filtering

### Prompt

Implement Feature 1 for the FastAPI Task Tracker: due dates and overdue filtering.

Requirements:

1. Add an optional `due_date` field using Python `date` to:
   - `TaskCreate`
   - `TaskUpdate`
   - `TaskResponse`

2. Add a reusable business-rule function:

   `is_task_overdue(due_date, task_status, today=None)`

   The function must return `True` only when:
   - a due date exists,
   - the due date is earlier than today,
   - the task status is not `Done`.

3. Update storage so that:
   - `due_date` is saved when a task is created,
   - PATCH updates can modify or clear `due_date`,
   - `get_all_tasks()` supports an optional `overdue` Boolean filter,
   - existing status and priority filters continue to work,
   - the existing `_reset()` test helper is preserved.

4. Preserve all existing CRUD behavior and status-transition rules.

5. Update existing tests so the response schema includes `due_date`.

6. Do not implement the frontend yet.

7. After implementation, run:

   `python -m compileall app`

   `python -m pytest -v`

Show the exact changes made and report the final verification results.

