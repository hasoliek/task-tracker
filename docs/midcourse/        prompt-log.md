# AI Prompt Log

This log records how AI tools were used during development of the FastAPI Task Tracker. It includes the prompts submitted, summaries of the AI responses, verification performed, and the human decision to accept, edit, or reject each response.

---

# Feature 1 — Due Dates and Overdue Filtering

## Prompt 1 — Review the Feature 1 design

### Prompt

Review the proposed Feature 1 design for the FastAPI Task Tracker.

Feature requirements:

- Tasks may have an optional due date.
- A task is overdue when its due date is before today and its status is not Done.
- Users must be able to filter tasks by overdue status.
- Existing CRUD behavior and status-transition rules must remain unchanged.

Identify assumptions, recommend a small implementation design, and identify any values that should be computed rather than stored.

### AI response summary

The AI recommended adding an optional `due_date` field to the task models. It also initially discussed storing an `overdue` value with each task.

### Human decision

**Edited**

### Reason

I accepted the optional due-date design but rejected storing `overdue` as a persistent field. A stored overdue value could become stale when the date changes.

The final design computes overdue status dynamically using:

- `due_date`,
- the current date,
- task status.

This design decision was recorded in the Mini-ADR.

---

## Prompt 2 — Update task models for due dates

### Prompt

Update `app/models.py` for Feature 1.

Requirements:

1. Import Python's `date` type.
2. Add an optional `due_date: date | None = None` field to:
   - `TaskCreate`,
   - `TaskUpdate`,
   - `TaskResponse`.
3. Preserve all existing:
   - status and priority enums,
   - title trimming,
   - blank-title validation,
   - extra-field rejection,
   - default values,
   - Pydantic configuration.
4. Do not change storage, routes, tests, or frontend yet.
5. Show the complete corrected file.

### AI response summary

The AI supplied an updated `models.py` containing the optional `due_date` field in the three task models.

### Human decision

**Edited**

### Reason

The AI response described the required update correctly, but the first generated workflow claimed that the file was updated when the actual file still did not contain all required changes.

I inspected the real file, corrected it, and verified that `due_date` existed in:

- `TaskCreate`,
- `TaskUpdate`,
- `TaskResponse`.

---

## Prompt 3 — Add the overdue business rule

### Prompt

Update `app/business_rules.py` for Feature 1.

Add a reusable function:

`is_task_overdue(due_date, task_status, today=None)`

Rules:

- Return `False` when no due date exists.
- Return `False` when status is `Done`.
- Return `False` when the due date is today.
- Return `True` only when the due date is earlier than today.
- Use the optional `today` argument to make the function testable.
- Preserve all existing status-transition validation rules.
- Show the complete corrected file.

### AI response summary

The AI added a centralized helper for calculating whether a task is overdue while preserving the status-transition rules.

### Human decision

**Edited**

### Reason

The design was accepted, but storage referenced the helper before the helper existed in the actual file. This caused an import error.

I inspected `app/business_rules.py`, added the missing helper, and confirmed that the import worked before continuing.

---

## Prompt 4 — Update storage for due dates and overdue filtering

### Prompt

Update `app/storage.py` for Feature 1.

Requirements:

1. Persist `due_date` when creating a task.
2. Allow PATCH updates to:
   - set a due date,
   - change a due date,
   - clear a due date.
3. Extend `get_all_tasks()` with:
   - `overdue: bool | None = None`.
4. Reuse `is_task_overdue()` instead of duplicating the overdue rule.
5. Preserve:
   - status filtering,
   - priority filtering,
   - CRUD behavior,
   - timestamps,
   - the `_reset()` helper required by pytest.
6. Show the complete corrected file.

### AI response summary

The AI added due-date persistence, due-date updates, and overdue filtering to the storage layer.

### Human decision

**Edited**

### Reason

The AI-generated storage file temporarily omitted `_reset()`. This caused the pytest fixture to fail.

I restored `_reset()` and verified that the existing CRUD test setup worked again.

---

## Prompt 5 — Update the list endpoint

### Prompt

Review the `GET /tasks` route in `app/main.py`.

The storage layer supports:

`get_all_tasks(status=None, priority=None, overdue=None)`

Update the route so that:

- it accepts `overdue: bool | None = None`,
- it forwards the value to storage,
- existing status and priority filtering remain unchanged,
- no unrelated route behavior is modified.

### AI response summary

The AI added the `overdue` query parameter and forwarded it to `storage.get_all_tasks()`.

### Human decision

**Accepted after verification**

### Reason

The correction was required after an overdue-filter test showed that both overdue and non-overdue tasks were returned. The storage layer supported the filter, but the route had not forwarded the query parameter.

After updating the route, the overdue filter behaved correctly.

---

## Prompt 6 — Update the response-schema test

### Prompt

Update `tests/test_tasks.py` because `TaskResponse` now includes `due_date`.

Requirements:

- Add `due_date` to the expected response keys in the valid task-creation test.
- Assert that `due_date` is `None` when it is not supplied.
- Preserve all existing assertions.
- Do not weaken the existing test.

### AI response summary

The AI updated the existing response-schema test to include the new optional field.

### Human decision

**Accepted**

### Reason

The change corrected the regression failure caused by the response containing one additional valid field.

---

## Prompt 7 — Add the due-date creation test

### Prompt

Add one pytest test for Feature 1 that:

- creates a task with a valid due date,
- expects HTTP 201,
- verifies that the returned due date matches the submitted ISO date.

Run only the new test before continuing.

### AI response summary

The AI added:

`test_create_task_with_due_date_returns_due_date`

### Human decision

**Accepted**

### Verification result

```text
1 passed, 17 deselected

Prompt 8 — Add the due-date update test

Prompt

Add one pytest test that:

* creates a task without a due date,
* updates it using PATCH,
* verifies that the due date is saved,
* verifies that unchanged fields are preserved.

Run only the new test before continuing.

AI response summary

The AI added:

test_patch_task_updates_due_date

Human decision

Accepted

Verification result
1 passed, 18 deselected
Prompt 9 — Add the overdue-filter test

Prompt

Add one pytest test that:

* creates one task with a past due date,
* creates one task with a future due date,
* requests GET /tasks?overdue=true,
* verifies that only the overdue task is returned.

Run only this test before continuing.

AI response summary

The AI added:

test_list_tasks_overdue_true_returns_only_overdue_tasks

Initial verification result
AssertionError: assert 2 == 1
Both tasks were returned instead of only the overdue task.

Human decision

Rejected initially, then edited

Reason

The test exposed an incomplete implementation. Storage supported overdue filtering, but the API route did not forward the query parameter.

I corrected app/main.py and reran the test.

Final result

The test passed after the route correction.

⸻

Prompt 10 — Add the completed-task overdue test

Prompt

Add one pytest test that:

* creates a task with a past due date,
* transitions it from ToDo to InProgress,
* transitions it from InProgress to Done,
* requests GET /tasks?overdue=true,
* verifies that the completed task is not returned.

Run only this test before continuing.

AI response summary

The AI added:

test_done_task_with_past_due_date_is_not_overdue

Human decision

Accepted

Verification result
1 passed, 20 deselected
Prompt 11 — Run the Feature 1 regression suite

Prompt

Run the complete pytest suite after all Feature 1 backend and test changes.

Confirm:

* all original tests still pass,
* all four new Feature 1 tests pass,
* the total collected test count is correct,
* warnings are recorded separately from failures.

AI response summary

The AI instructed me to run the full test suite and distinguish warnings from failures.

Human decision

Accepted

Verification result
21 passed, 3 warnings in 0.04s
Prompt 12 — Integrate due dates into the frontend

Prompt

Update frontend/index.html for Feature 1.

Requirements:

1. Add an optional date input to the create/edit form.
2. Send the value to the backend using the JSON field due_date.
3. Send null when the input is empty.
4. Load the existing due date when editing a task.
5. Display the due date on task cards.
6. Preserve:
    * task creation,
    * task editing,
    * drag-and-drop status updates,
    * title validation,
    * the existing board layout.
7. Provide the complete corrected index.html.

AI response summary

The AI generated frontend support for:

* entering due dates,
* sending due dates in requests,
* loading due dates during editing,
* clearing due dates,
* displaying due dates on task cards.

Human decision

Edited

Reason

The initial frontend version did not completely connect every modal element and payload field. I inspected the real file and corrected the missing references before manual testing.

⸻

Prompt 13 — Verify frontend task creation

Prompt

Manually create a task through the frontend with:

* title,
* description,
* priority,
* assignee,
* a future due date.

Verify that:

* the request succeeds,
* the task appears on the Kanban board,
* the selected due date appears on the task card.

AI response summary

The AI provided a manual verification checklist.

Human decision

Accepted

Manual verification result

The task was created successfully and displayed with:

* Title: Task 1
* Description: Testing due date
* Priority: High
* Assignee: Hassan
* Due date: 2026-07-23

⸻

Prompt 14 — Verify existing frontend validation

Prompt

Attempt to create a task with:

* a blank title,
* a description,
* a valid due date.

Verify that:

* the task is not created,
* the modal remains open,
* the message Title is required is displayed.

AI response summary

The AI provided the expected validation behavior.

Human decision

Accepted

Manual verification result

The modal remained open, the task was not created, and the expected validation message appeared.

⸻

Feature 2 — Tags and Tag Filtering

Prompt 15 — Add tag styles

Prompt

Update only frontend/index.html.

Add CSS styles for task tags without changing existing styles.

Requirements:

* Add a .card-tags container.
* Add a .tag-chip style.
* Display tags as rounded blue chips below the task metadata.
* Do not modify JavaScript yet.

AI response summary

The AI added the requested CSS classes for tag layout and tag chips.

Human decision

Accepted

Reason

The styles were isolated and did not modify unrelated frontend behavior.

⸻

Prompt 16 — Add the Tags field to the modal

Prompt

Update only frontend/index.html.

In the task modal, add a Tags input immediately below the Due Date field.

Requirements:

* id="task-tags"
* type="text"
* placeholder="backend, urgent, testing"
* helper text: Separate multiple tags with commas.
* Do not modify JavaScript.

AI response summary

The AI added the Tags input and helper text to the task modal.

Human decision

Accepted

⸻

Prompt 17 — Display tags on task cards

Prompt

Update only frontend/index.html.

Modify taskCardHtml().

Requirements:

* If task.tags contains values, display every tag as a blue chip below the task metadata.
* If there are no tags, display No tags.
* Do not modify any other functions.

AI response summary

The AI updated the task-card rendering logic to display tag chips or a no-tags message.

Human decision

Accepted

⸻

Prompt 18 — Add the Tags element reference

Prompt

Update only frontend/index.html.

Modify getModalElements().

Add:
taskTags: document.getElementById("task-tags")
Do not change anything else.

AI response summary

The AI added the Tags input reference to the modal element collection.

Human decision

Accepted

⸻

Prompt 19 — Load tags when editing

Prompt

Update only frontend/index.html.

Modify openEditModal().

When a task is opened for editing, populate the Tags field.

Requirements:

* If task.tags exists, join the values using ", ".
* Example: backend, urgent, testing
* If no tags exist, leave the field empty.
* Do not change any other logic.

AI response summary

The AI updated the edit modal so existing task tags were loaded as comma-separated text.

Human decision

Accepted

⸻

Prompt 20 — Submit tags through POST and PATCH

Initial weak prompt

Add tags to the task form.

Improved prompt

Update only frontend/index.html.

Modify handleTaskFormSubmit().

Requirements:

1. Read the value from taskTags.
2. Split the input using commas.
3. Trim whitespace from every tag.
4. Remove duplicate nonblank tags.
5. Store the result in a variable named tags.
6. Include tags in both POST and PATCH payloads.
7. Preserve:
    * due-date handling,
    * title validation,
    * modal behavior,
    * drag-and-drop,
    * existing filters.
8. Do not refactor unrelated code.

Why the improved prompt is stronger

The initial prompt did not specify:

* which file to update,
* which function to change,
* how tags should be parsed,
* whether tags must be included in POST and PATCH,
* which existing behaviors must remain unchanged.

The improved prompt defined the target, constraints, acceptance criteria, and required behavior.

AI response summary

The AI added tag parsing and included tags in task-creation and task-update requests.

Human decision

Edited

Reason

The initial implementation silently ignored blank entries. This behavior was later changed because the reviewer required blank tags to be rejected rather than silently removed.

⸻

Prompt 21 — Add a tag filter input

Prompt

Update only frontend/index.html.

Add a Tag filter textbox beside the existing Overdue filter.

Requirements:

* id="tag-filter"
* placeholder="Filter by tag"
* Do not modify JavaScript yet.

AI response summary

The AI added the tag-filter input beside the overdue filter.

Human decision

Accepted

⸻

Prompt 22 — Forward the tag filter to the API

Prompt

Update only frontend/index.html.

Modify fetchTasks().

Requirements:

* If the Tag filter contains text, send ?tag=value.
* If both Overdue and Tag filters are active, send:
    ?overdue=true&tag=value
* Trim whitespace from the tag-filter input.
* Use safe URL encoding.
* Keep all existing filtering behavior intact.

AI response summary

The AI updated fetchTasks() to build the query string for overdue and tag filtering.

Human decision

Accepted after manual verification

⸻

Prompt 23 — Reload the board when the tag filter changes

Prompt

Update only frontend/index.html.

Whenever the Tag filter text changes, automatically reload the board.

Requirements:

* Keep the existing Overdue filter behavior.
* Do not modify any unrelated functionality.

AI response summary

The AI added an input event listener that reloads tasks when the tag-filter value changes.

Human decision

Accepted

⸻

Prompt 24 — Review Feature 2 frontend behavior

Prompt

Review frontend/index.html.

Verify:

* creating tasks with tags works,
* editing tags works,
* clearing tags works,
* tag chips display correctly,
* tag filtering works,
* overdue filtering still works,
* combined overdue and tag filtering works,
* drag-and-drop still works.

Only fix issues that are found.

Do not refactor unrelated code.

AI response summary

The AI reviewed the related frontend functions and identified missing connections between:

* the due-date field,
* the Tags field,
* POST and PATCH payloads,
* task-card rendering.

Human decision

Edited

Reason

Some parts of the implementation existed in the interface but were not fully connected to submission and editing logic. I corrected the missing references and retested the frontend.

⸻

Reviewer Feedback Corrections

Prompt 25 — Fix frontend modal submission after review

Initial weak prompt

Update the frontend to support tags and due dates.

Improved prompt

Update only frontend/index.html.

Requirements:

* Include due_date in both POST and PATCH payloads.
* Include tags in both POST and PATCH payloads.
* Load the existing due date and tags when editing.
* Allow tags and due dates to be cleared.
* Preserve all existing validation.
* Do not modify unrelated JavaScript.
* Return only the modified sections.

AI response summary

The AI corrected the modal submission logic so due dates and tags were included in both create and update requests.

Human decision

Accepted after inspection

Reason

The correction addressed the reviewer’s observation that the modal did not submit the new fields.

⸻

Prompt 26 — Display due dates and overdue state on cards

Prompt

Update only frontend/index.html.

Modify task-card rendering.

Requirements:

* Display the task due date when one exists.
* Display a visible overdue indicator when:
    * the due date is before today,
    * the task status is not Done.
* Do not show an overdue indicator for completed tasks.
* Preserve tag chips and existing card actions.
* Do not modify unrelated functions.

AI response summary

The AI added due-date text and an overdue indicator to task cards.

Human decision

Accepted after manual verification

Reason

This directly addressed the reviewer’s comment that cards did not display due dates or overdue status.

⸻

Prompt 27 — Reject blank tags instead of silently removing them

Initial weak prompt

Clean tags before saving.

Improved prompt

Update tag validation without changing unrelated behavior.

Requirements:

* Split comma-separated input into individual tags.
* Trim each tag.
* Reject submission if an explicitly entered tag is empty after trimming.
* Do not silently discard blank tag entries.
* Remove duplicate nonblank tags.
* Keep the modal open when validation fails.
* Display a clear validation message.
* Enforce the same rule in backend validation.
* Preserve the ability to clear all tags by submitting an empty tag list.

AI response summary

The AI initially continued to filter blank tags out silently.

Human decision

Rejected initially, then edited

Reason

Silently removing blank tags did not satisfy the reviewer’s requirement.

I changed the behavior so blank entries inside a submitted tag list are rejected with HTTP 422. A valid empty list remains allowed when the user intentionally clears all tags.

⸻

Prompt 28 — Add explicit-null regression tests

Initial weak prompt

Add regression tests.

Improved prompt

Update only tests/test_tasks.py.

Add regression tests for explicit null validation.

Requirements:

1. Confirm POST /tasks rejects:
    * {"title": null}
        with HTTP 422.
2. Confirm PATCH rejects:
    * {"title": null},
    * {"status": null},
    * {"priority": null}.
3. Create a real task before the PATCH requests.
4. Confirm omitted fields remain allowed during PATCH.
5. Do not modify:
    * app/models.py,
    * app/main.py,
    * storage,
    * frontend.
6. Follow the existing pytest structure.

AI response summary

The AI attempted to add the regression tests but inserted pytest functions into app/models.py.

This caused application import to fail with:
NameError: name 'pytest' is not defined
Human decision

Rejected

Reason

The AI modified the wrong file and mixed test code with production model code.

I removed the test functions from app/models.py and placed the tests in tests/test_tasks.py.

This was an important example of why AI-generated changes must be inspected before acceptance.

⸻

Prompt 29 — Restore the production models file

Prompt

Restore app/models.py.

Requirements:

* Remove all pytest imports, decorators, fixtures, and test functions.
* Keep only:
    * imports used by the models,
    * TaskStatus,
    * TaskPriority,
    * tag-cleaning or validation helpers,
    * TaskCreate,
    * TaskUpdate,
    * TaskResponse.
* Preserve due-date and tag fields.
* Do not add any test code.

AI response summary

The AI supplied a clean version of app/models.py without pytest code.

Human decision

Accepted after manual comparison

Reason

The file returned to its correct responsibility: production data validation only.

⸻

Prompt 30 — Restore TaskCreate defaults

Prompt

Update TaskCreate so omitted fields preserve the existing API contract.

Requirements:

* status defaults to ToDo,
* priority defaults to Medium,
* explicit null must still be rejected,
* preserve due-date and tag fields,
* preserve existing validation.

AI response summary

The AI restored the default values for status and priority.

Human decision

Accepted

Reason

Without these defaults, many existing tests failed because they created tasks using only a title or a title with optional fields.

After restoring the defaults, most failures were resolved.

⸻

Prompt 31 — Add complete model validation

Prompt

Update app/models.py.

Requirements:

* reject blank or whitespace-only titles,
* trim valid titles,
* reject unknown fields,
* reject blank tags,
* trim valid tags,
* remove duplicate valid tags,
* preserve tag order,
* preserve the ability to clear tags with an empty list,
* preserve default status and priority,
* preserve due-date support,
* reject explicit null values for required fields.

AI response summary

The AI added:

* ConfigDict(extra="forbid"),
* title validation,
* tag validation,
* duplicate removal,
* whitespace trimming.

Human decision

Edited

Reason

The validator design was accepted, but the test suite still contained older expectations that blank tags should be silently removed.

I updated those tests to align with the reviewer-required business rule.

⸻

Prompt 32 — Update outdated tag tests

Prompt

Update only tests/test_tasks.py.

Requirements:

1. Modify the tag-cleaning test so it verifies:
    * whitespace trimming,
    * duplicate removal,
    * original order preservation.
2. Do not include blank tags in the successful cleaning test.
3. Add a separate test confirming blank tags return HTTP 422.
4. Preserve the test for clearing tags with an empty list.
5. Do not modify application code.

AI response summary

The AI separated valid tag normalization from invalid blank-tag behavior.

Human decision

Accepted after correction

Reason

The first test still contained:
""
"   "
which correctly caused HTTP 422 under the new rule. I removed those values from the successful cleaning test and kept blank-tag rejection in its own test.

⸻

Prompt 33 — Verify explicit-null behavior manually

Prompt

Use curl to verify backend validation.

Tests:

1. POST a task with "title": null.
2. PATCH an existing task with "title": null.
3. PATCH an existing task with "status": null.
4. PATCH an existing task with "priority": null.

Expected result:

* HTTP 422 for every request.

AI response summary

The AI provided curl commands for manual validation.

Human decision

Accepted

Manual verification result

The backend returned HTTP 422 for:

* null title during creation,
* null title during update,
* null status during update,
* null priority during update.

This confirmed that explicit null values were rejected.

⸻

Prompt 34 — Run the final regression suite

Prompt

Run the complete pytest suite after all reviewer corrections.

Confirm:

* task creation works with default status and priority,
* blank titles are rejected,
* unknown fields are rejected,
* due dates can be created and updated,
* overdue filtering works,
* completed tasks are not overdue,
* tags are trimmed,
* duplicate tags are removed,
* blank tags are rejected,
* tags can be cleared,
* tag filtering works,
* explicit null values are rejected,
* omitted PATCH fields remain allowed,
* all existing CRUD and status-transition tests still pass.

Record warnings separately from failures.

AI response summary

The AI instructed me to run the full regression suite and verify that warnings did not represent test failures.

Human decision

Accepted

Final verification result
37 passed, 3 warnings in 0.10s
The warnings were:

* a Starlette TestClient dependency deprecation warning,
* two FastAPI/Starlette HTTP 422 constant deprecation warnings.

There were no functional test failures.

⸻

Prompting Reflection

The project demonstrated that broad prompts often produced incomplete or overly wide changes. The most effective prompts specified:

* the exact file to modify,
* the exact function or class to change,
* required behavior,
* behavior that must remain unchanged,
* acceptance criteria,
* files that must not be modified.

For example, the weak prompt:

Add regression tests.

allowed the AI to place test code in the wrong file.

The improved prompt explicitly required:

* updating only tests/test_tasks.py,
* avoiding all production files,
* creating a real task before PATCH tests,
* verifying both null rejection and omitted-field support.

Even with these constraints, the generated output still required inspection. The incorrect modification to app/models.py was rejected, restored manually, and verified through pytest.

The final workflow was:

1. submit a narrowly scoped prompt,
2. inspect the actual changed file,
3. run one focused test,
4. correct the root cause,
5. run the complete regression suite,
6. record whether the AI response was accepted, edited, or rejected.

