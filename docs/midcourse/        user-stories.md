User Stories (Feature 1)
Story 1

Story

As a team member, I want to assign an optional due date when creating a task so that I can keep track of task deadlines.

Acceptance Criteria

* A task can be created with or without a due date.
* The due date must be a valid calendar date in the supported format.
* An invalid due date returns HTTP 422 with a validation error.
* A task created with a due date stores and returns the due date correctly.
* A task created without a due date is created successfully.

⸻

Story 2

Story

As a team member, I want to update or remove a task’s due date so that I can keep task deadlines accurate.

Acceptance Criteria

* A due date can be added to a task that does not already have one.
* An existing due date can be updated.
* A due date can be removed without deleting the task.
* Updating or removing the due date does not modify other task fields.
* Updating a task that does not exist returns HTTP 404.

⸻

Story 3

Story

As a team member, I want overdue tasks to be identified automatically so that I can quickly recognize work requiring attention.

Acceptance Criteria

* A task is considered overdue only if it has a due date before the current date.
* Tasks with status Done are never considered overdue.
* Tasks due on the current date are not considered overdue.
* Tasks without a due date are never considered overdue.
* Overdue status is determined automatically without requiring manual updates.

⸻

Story 4

Story

As a team member, I want to filter tasks to display only overdue tasks so that I can focus on work requiring immediate attention.

Acceptance Criteria

* Applying the overdue filter returns only overdue tasks.
* If no overdue tasks exist, the API returns HTTP 200 with an empty list.
* Removing the overdue filter restores the complete task list.
* The frontend provides a clear way to enable and disable the overdue filter.
* Invalid filter values return HTTP 422 if validated by the backend.

User Stories (Feature 2)
Story 1

Story

As a team member, I want to add one or more tags to a task so that I can organize tasks by category.

Acceptance Criteria

* A task can be created with zero or more tags.
* Each tag must contain non-blank text after trimming.
* A task created with valid tags stores and returns the tags correctly.
* A task created without tags is created successfully with an empty tag list.
* A blank tag returns HTTP 422 with a validation error.

⸻

Story 2

Story

As a team member, I want to update or remove a task’s tags so that its categorization remains accurate.

Acceptance Criteria

* Tags can be added to an existing task.
* Existing tags can be replaced with a different list of tags.
* All tags can be removed by updating the task with an empty tag list.
* Updating tags does not modify unrelated task fields.
* Updating a task that does not exist returns HTTP 404.

⸻

Story 3

Story

As a team member, I want tags to be displayed on each task card so that I can quickly identify related tasks.

Acceptance Criteria

* Each task card displays all tags assigned to the task.
* Tasks without tags continue to display normally.
* Tags are shown in a clear and readable format.
* Updating a task’s tags updates the tags shown on its card after the task list is refreshed.
* Tag display does not change the task’s status, priority, assignee, or description.

⸻

Story 4

Story

As a team member, I want to filter tasks by tag so that I can focus on tasks in a specific category.

Acceptance Criteria

* Applying a tag filter returns only tasks containing the selected tag.
* Tag filtering matches complete tag values rather than partial text.
* If no tasks match the selected tag, the API returns HTTP 200 with an empty list.
* Removing the tag filter restores the complete task list.
* Tags are preserved when an unrelated task field is updated.

Feature 1 – Due Dates + Overdue Filter
ID

Story

Acceptance Criteria

Notes / Assumptions

US-1

As a team member, I want to assign an optional due date when creating a task so that I can keep track of task deadlines.

• A task can be created with or without a due date.• The due date must be a valid calendar date in the supported format.• An invalid due date returns HTTP 422 with a validation error.• A task created with a due date stores and returns the due date correctly.• A task created without a due date is created successfully.

Assumes the due date is optional and follows a standard calendar date format (YYYY-MM-DD).

US-2

As a team member, I want to update or remove a task’s due date so that I can keep task deadlines accurate.

• A due date can be added to a task that does not already have one.• An existing due date can be updated.• A due date can be removed without deleting the task.• Updating or removing the due date does not modify other task fields.• Updating a task that does not exist returns HTTP 404.

Assumes partial task updates are supported through the existing PATCH endpoint.

US-3

As a team member, I want overdue tasks to be identified automatically so that I can quickly recognize work requiring attention.

• A task is overdue only if it has a due date before the current date.• Tasks with status Done are never overdue.• Tasks due on the current date are not considered overdue.• Tasks without a due date are never considered overdue.• Overdue status is determined automatically.

Assumes overdue is calculated dynamically rather than stored permanently.

US-4

As a team member, I want to filter tasks to display only overdue tasks so that I can focus on work requiring immediate attention.

• Applying the overdue filter returns only overdue tasks.• If no overdue tasks exist, the API returns HTTP 200 with an empty list.• Removing the overdue filter restores the complete task list.• The frontend provides a clear way to enable and disable the overdue filter.• Invalid filter values return HTTP 422 if validated by the backend.

Assumes overdue filtering is supported by the backend and exposed through the frontend.

## AI Assumption Corrected

### Feature 1

AI initially suggested storing an `overdue` field in every task.

After reviewing the design, this assumption was rejected because overdue status changes automatically as time passes. Instead, overdue will be calculated dynamically from the task's due date and current status.

Feature 2 – Tags / Labels
ID

Story

Acceptance Criteria

Notes / Assumptions

US-1

As a team member, I want to add one or more tags to a task so that I can organize tasks by category.

• A task can be created with zero or more tags.• Each tag must contain non-blank text after trimming.• A task created with valid tags stores and returns the tags correctly.• A task created without tags is created successfully with an empty tag list.• A blank tag returns HTTP 422 with a validation error.

Assumes tags are stored as a list of strings and leading/trailing spaces are removed.

US-2

As a team member, I want to update or remove a task’s tags so that its categorization remains accurate.

• Tags can be added to an existing task.• Existing tags can be replaced with a different list of tags.• All tags can be removed by updating the task with an empty tag list.• Updating tags does not modify unrelated task fields.• Updating a task that does not exist returns HTTP 404.

Assumes existing PATCH behavior supports partial updates while preserving unrelated fields.

US-3

As a team member, I want tags to be displayed on each task card so that I can quickly identify related tasks.

• Each task card displays all assigned tags.• Tasks without tags continue to display normally.• Tags are presented in a clear and readable format.• Updating tags refreshes the displayed task information.• Tag display does not affect other task properties.

Assumes tags are rendered as visual labels (chips or badges) in the existing Kanban cards.

US-4

As a team member, I want to filter tasks by tag so that I can focus on tasks in a specific category.

• Applying a tag filter returns only tasks containing the selected tag.• Tag filtering matches complete tag values.• If no tasks match, the API returns HTTP 200 with an empty list.• Removing the tag filter restores the complete task list.• Tags remain unchanged when unrelated task fields are updated.

Assumes filtering is performed using exact tag matching and integrates with the existing task list view.

## AI Assumption Corrected

### Feature 2

AI initially suggested storing tags as a comma-separated string.

After reviewing the implementation, this assumption was rejected because it complicates validation and filtering. Tags will instead be stored as a list of strings.