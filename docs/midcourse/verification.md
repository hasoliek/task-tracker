## Automated Verification
# Verification Log

## Baseline Verification

Before implementing the mid-course project features, the existing Task Tracker application was verified to ensure a stable baseline for development. This established that all existing functionality worked correctly before introducing any new changes.

The following baseline functionality was verified:

- FastAPI application started successfully.
- Health endpoint responded correctly.
- Swagger/OpenAPI documentation loaded successfully.
- Frontend loaded correctly using VS Code Live Server.
- Existing CRUD operations worked correctly.
- Existing status transitions behaved as expected.
- Existing filtering functionality remained operational.
- Existing automated regression tests completed successfully.

### Baseline Result

```text
17 passed
```

**Status:** Passed.

---

# Feature 1 — Due Dates and Overdue Filtering

## Model Verification

The data models were updated to support optional due dates while preserving all existing validation behavior.

Verified that:

- `TaskCreate` accepts an optional `due_date`.
- `TaskUpdate` accepts an optional `due_date`.
- `TaskResponse` returns the stored `due_date`.
- Existing default values remain unchanged.
- Existing status validation remains unchanged.
- Existing priority validation remains unchanged.
- Blank-title validation continues to reject invalid requests.
- Unknown request fields continue to return validation errors.
- Invalid date formats are rejected automatically by Pydantic validation.

**Status:** Passed.

---

## Business Rule Verification

Overdue status is calculated dynamically rather than stored as part of the task model.

A task is considered overdue only when:

- a due date exists,
- the due date is earlier than the current date,
- the task status is not `Done`.

Verified that:

- tasks without due dates are not overdue,
- future due dates are not overdue,
- tasks due today are not considered overdue,
- completed tasks are never considered overdue,
- overdue status updates automatically without modifying stored task data.

**Status:** Passed.

---

## Storage Verification

Verified that the storage layer correctly manages due-date information.

Confirmed that:

- due dates are stored during task creation,
- due dates can be modified through PATCH requests,
- due dates can be cleared,
- overdue filtering uses the shared overdue business-rule helper,
- status filtering continues to function correctly,
- priority filtering continues to function correctly,
- timestamps continue updating correctly,
- the storage reset helper (`_reset()`) remains available for automated test isolation.

**Status:** Passed.

---

## API Verification

Verified the backend REST API for Feature 1.

Confirmed that:

- `POST /tasks` accepts and returns `due_date`,
- `PATCH /tasks/{task_id}` updates due dates correctly,
- due dates may be removed by submitting a null optional value where supported,
- `GET /tasks?overdue=true` returns only overdue active tasks,
- completed tasks are excluded from overdue results,
- overdue filtering works together with existing status and priority filters,
- existing CRUD behavior remains unchanged.

**Status:** Passed.

---

## Frontend Verification

Verified that the frontend correctly integrates the new due-date functionality.

Confirmed that:

- the task modal includes a Due Date field,
- due dates are submitted during task creation,
- due dates are submitted during task editing,
- existing due dates load correctly when editing tasks,
- clearing a due date removes it successfully,
- due dates display correctly on task cards,
- overdue indicators appear only for overdue active tasks,
- completed tasks no longer display overdue indicators.

**Status:** Passed.

---

## Automated Test Verification

The following automated regression tests were implemented for Feature 1:

- `test_create_task_with_due_date_returns_due_date`
- `test_patch_task_updates_due_date`
- `test_list_tasks_overdue_true_returns_only_overdue_tasks`
- `test_done_task_with_past_due_date_is_not_overdue`

During implementation, the overdue-filter test initially exposed a regression:

```text
FAILED test_list_tasks_overdue_true_returns_only_overdue_tasks

AssertionError:
assert 2 == 1
```

Investigation showed that the API endpoint was not forwarding the `overdue` query parameter to the storage layer. After correcting the route, the affected test passed and the complete regression suite remained successful.

**Status:** Passed.

---

# Feature 2 — Tags and Tag Filtering

## Model Verification

The task models were extended to support tag management while preserving existing validation behavior.

Verified that:

- `TaskCreate` accepts an optional list of tags,
- `TaskUpdate` accepts optional tag updates,
- `TaskResponse` returns stored tags,
- existing validation behavior remains unchanged,
- explicit null values for required fields continue to be rejected,
- unknown request fields continue returning validation errors.

**Status:** Passed.

---

## Business Rule Verification

Verified that tag processing follows the required business rules.

Confirmed that:

- surrounding whitespace is removed,
- duplicate tags are removed while preserving order,
- blank or whitespace-only tags are rejected,
- an empty tag list is accepted when clearing tags,
- omitted tags during PATCH requests leave existing tags unchanged.

**Status:** Passed.

---

## Storage Verification

Verified correct storage behavior for task tags.

Confirmed that:

- tags are stored during task creation,
- tags are updated during PATCH requests,
- tags can be removed,
- duplicate tags are not stored,
- existing task data remains unchanged when tags are omitted,
- filtering by tag returns only matching tasks.

**Status:** Passed.

---

## API Verification

Verified backend API behavior for tag functionality.

Confirmed that:

- `POST /tasks` accepts tags,
- `PATCH /tasks/{task_id}` updates tags,
- `GET /tasks?tag=value` filters matching tasks,
- blank tags return HTTP 422,
- duplicate tags are normalized,
- tag filtering operates correctly together with overdue filtering.

**Status:** Passed.

---

## Frontend Verification

Verified that the frontend correctly supports tag management.

Confirmed that:

- the task modal includes a Tags field,
- existing tags load correctly while editing,
- tags are submitted during POST requests,
- tags are submitted during PATCH requests,
- tag chips display correctly on task cards,
- tags can be edited,
- tags can be cleared,
- tag filtering updates the displayed task list,
- combined overdue and tag filtering behaves correctly.

**Status:** Passed.

---

## Automated Test Verification

Automated regression tests verified:

- tag normalization,
- duplicate removal,
- blank-tag rejection,
- tag updates,
- clearing tags,
- tag filtering,
- regression behavior after validation changes.

Additional regression tests confirmed that stricter validation did not affect unrelated CRUD operations.

**Status:** Passed.

---

# Manual Browser Verification

The application was manually tested using the FastAPI backend together with the frontend served through VS Code Live Server.

The following end-to-end workflows were verified successfully.

| Workflow | Observed Result | Status |
|-----------|-----------------|--------|
| Create a task | Task was created successfully and appeared on the Kanban board. | Passed |
| Edit a task | Changes were saved and immediately reflected on the board. | Passed |
| Delete a task | Task was removed successfully. | Passed |
| Move a task between Kanban columns | Status updated correctly and persisted after refresh. | Passed |
| Create a task with a due date | Due date was saved and displayed correctly. | Passed |
| Edit a due date | Updated due date appeared immediately after saving. | Passed |
| Clear a due date | Due date was removed successfully from the task card. | Passed |
| Create a task with tags | Tags appeared correctly as task chips. | Passed |
| Edit tags | Updated tags replaced the previous values correctly. | Passed |
| Clear tags | Task displayed no tags after saving. | Passed |
| Filter by overdue | Only overdue active tasks were displayed. | Passed |
| Filter by tag | Only tasks containing the selected tag were displayed. | Passed |
| Combine overdue and tag filters | Only tasks matching both filters remained visible. | Passed |
| Existing validation | Blank titles continued to be rejected and status transitions remained unchanged. | Passed |

All manual workflows behaved as expected. No inconsistencies were observed between the frontend user interface and the backend API responses.

**Status:** Passed.

# Regression Investigation (Break Tests)

During development, several regressions were identified through automated testing while implementing the new functionality. Each regression was investigated to determine the root cause, corrected in the implementation, and verified by rerunning the affected tests together with the complete regression suite.

These investigations provided confidence that the new features did not introduce unintended side effects into the existing application.

---

## Break Test 1 — Overdue Filter Regression

### Objective

Verify that the overdue filter returns only active overdue tasks.

### Regression Observed

During implementation, the automated test:

`test_list_tasks_overdue_true_returns_only_overdue_tasks`

initially failed with:

```text
FAILED test_list_tasks_overdue_true_returns_only_overdue_tasks

AssertionError:
assert 2 == 1
```

### Root Cause

Investigation showed that the `GET /tasks` endpoint was not forwarding the `overdue` query parameter to the storage layer. As a result, the storage logic returned both overdue and non-overdue tasks instead of applying the requested filter.

### Resolution

The route implementation was corrected to forward the `overdue` parameter to the storage layer, allowing the existing overdue business-rule helper to perform the filtering correctly.

### Verification

The affected regression test passed after the correction, and the complete regression suite continued to pass successfully.

**Status:** Passed.

---

## Break Test 2 — Blank Tag Validation Regression

### Objective

Verify that blank tags are rejected instead of being silently removed.

### Regression Observed

After implementing stricter tag validation, an existing tag-normalization test failed because it still expected blank tags to be ignored.

### Root Cause

The original test reflected the previous implementation. The updated acceptance criteria required blank or whitespace-only tags to produce an HTTP 422 validation error instead of being silently discarded.

### Resolution

The validation helper was updated to reject blank tags, the normalization test was revised to contain only valid tags, and a dedicated regression test was added to verify HTTP 422 behavior for blank tags.

### Verification

The updated regression tests confirmed that:

- valid tags are trimmed,
- duplicate tags are removed,
- blank tags return HTTP 422,
- clearing tags continues to function correctly.

**Status:** Passed.

---

## Break Test 3 — Explicit Null Validation Regression

### Objective

Verify that required task fields reject explicit `null` values while optional fields continue to behave correctly.

### Regression Observed

During reviewer-requested improvements, validation behavior was updated to distinguish omitted fields from explicitly supplied `null` values.

Additional automated tests exposed cases where explicit `null` values were incorrectly accepted for required fields.

### Root Cause

Validation logic did not consistently distinguish between omitted request fields and fields explicitly assigned a `null` value during partial updates.

### Resolution

Validation was updated to reject explicit `null` values for required fields while preserving the intended PATCH semantics for optional fields.

Additional regression tests were added covering:

- `title: null`
- `status: null`
- `priority: null`

### Verification

The updated validation correctly returned HTTP 422 for explicit `null` values while preserving existing PATCH behavior for omitted fields.

**Status:** Passed.

---

# Behavior Contract Before and After Refactoring

## Objective

The implementation was refactored to introduce Due Dates, Overdue Filtering, and Tags while preserving all existing task-management functionality.

The objective of the refactor was to extend the application without introducing regressions into the existing CRUD behavior or API contract.

---

## Existing Behavior Before Refactoring

Before implementing the new features, the application already supported:

- task creation,
- task editing,
- task deletion,
- Kanban status transitions,
- status filtering,
- priority filtering,
- partial PATCH updates,
- REST API CRUD operations.

These behaviors were considered the existing contract and were required to remain unchanged.

---

## New Behavior Introduced

The refactor added:

### Feature 1

- optional due dates,
- automatic overdue detection,
- overdue filtering,
- overdue indicators in the frontend.

### Feature 2

- task tags,
- tag normalization,
- duplicate removal,
- blank-tag validation,
- tag filtering,
- tag display within task cards.

---

## Contract Verification

The following existing behaviors were verified after the refactor:

- CRUD operations remained unchanged.
- Existing API endpoints continued to function.
- Existing response formats remained unchanged except for the newly introduced fields.
- Existing status transitions behaved correctly.
- Existing priority filtering behaved correctly.
- PATCH updates continued to support partial modifications.
- Drag-and-drop functionality continued to operate correctly.
- Existing automated regression tests continued to pass.

The following new behaviors were verified:

- due-date creation,
- due-date updates,
- overdue filtering,
- overdue indicators,
- tag creation,
- tag updates,
- tag clearing,
- tag filtering,
- blank-tag validation,
- explicit null validation.

No regressions were identified following the refactor.

**Status:** Passed.

---

# Final Regression Verification

After completing both feature implementations and resolving all identified regressions, the complete automated regression suite was executed.

The following categories were verified:

- baseline functionality,
- Feature 1 automated tests,
- Feature 2 automated tests,
- existing CRUD operations,
- API validation,
- frontend integration,
- manual browser verification,
- regression investigations,
- reviewer-requested validation improvements.

Final pytest result:

```text
37 passed, 3 warnings
```

The reported warnings were dependency and deprecation warnings only and did not affect application functionality.

No functional regressions were identified.

**Status:** Passed.

---

# Verification Summary

The completed implementation was verified using a combination of automated regression testing, API validation, frontend verification, manual browser testing, and regression investigation throughout development.

Verification activities included:

- Baseline verification
- Feature 1 verification
- Feature 2 verification
- Model verification
- Business-rule verification
- Storage verification
- API verification
- Frontend verification
- Manual browser verification
- Three documented regression investigations
- Behavior contract verification
- Complete regression testing

## Overall Verification Result

The Task Tracker application successfully implements the required mid-course features while preserving the existing functionality of the application.

The completed verification confirms that:

- Feature 1 (Due Dates and Overdue Filtering) operates correctly.
- Feature 2 (Tags and Tag Filtering) operates correctly.
- Existing CRUD functionality was preserved.
- Existing API behavior remained compatible.
- Reviewer-requested validation improvements were implemented successfully.
- No functional regressions were introduced.

Final automated verification result:

```text
37 passed, 3 warnings
```

The implementation satisfies the defined acceptance criteria and completed verification with no functional regressions identified.git add docs/midcourse/verification.md
