Feature 1 – Due Dates and Overdue Filter

ID

User Story

Acceptance Criteria

Notes / Assumptions

US-1

As a team member, I want to assign an optional due date when creating a task so that I can keep track of task deadlines.

• A task can be created with or without a due date.• The due date must be a valid YYYY-MM-DD date.• Invalid dates return HTTP 422.• Due dates are stored and returned correctly.

Due dates are optional.

US-2

As a team member, I want to update or remove a task’s due date so that I can keep deadlines accurate.

• Due dates can be added, changed, or removed.• Other task fields remain unchanged.• Missing tasks return HTTP 404.

Uses the existing PATCH endpoint.

US-3

As a team member, I want overdue tasks to be identified automatically so that I can quickly recognize work requiring attention.

• A task is overdue only if its due date is before today and its status is not Done.• Tasks due today are not overdue.• Tasks without due dates are never overdue.

Overdue is computed dynamically and is not stored.

US-4

As a team member, I want to filter tasks to display only overdue tasks so that I can focus on work requiring immediate attention.

• Only overdue tasks are returned.• Empty results return HTTP 200.• Removing the filter restores all tasks.

Filtering is implemented through the backend API and exposed in the frontend.

AI Assumption Corrected

Initially, AI suggested storing an overdue field in every task.

This approach was rejected because overdue status changes automatically as time passes. Instead, overdue is calculated dynamically from the task’s due date and current task status.

Feature 2 – Tags and Tag Filtering
ID

User Story

Acceptance Criteria

Notes / Assumptions

US-5

As a team member, I want to add one or more tags to a task so that I can organize tasks by category.

• Tasks may contain zero or more tags.• Blank tags are rejected after trimming.• Valid tags are stored and returned correctly.

Tags are stored as a list of strings.

US-6

As a team member, I want to update or remove a task’s tags so that task categorization remains accurate.

• Tags can be added, replaced, or removed.• Other task fields remain unchanged.• Missing tasks return HTTP 404.

Uses the existing PATCH endpoint.

US-7

As a team member, I want task tags to be displayed on each Kanban card so that I can quickly identify related work.

• All assigned tags are displayed.• Tasks without tags still display normally.• Updating tags updates the card display.

Tags are rendered as visual chips on each task card.

US-8

As a team member, I want to filter tasks by tag so that I can focus on tasks in a specific category.

• Filtering returns only tasks containing the selected tag.• Exact tag matching is used.• Removing the filter restores the full task list.

Tag filtering is supported by both the backend and frontend.
AI Assumption Corrected

Initially, AI suggested storing tags as a comma-separated string.

This approach was rejected because it complicates validation and filtering. Tags are stored as a list of strings, making validation, updates, and filtering simpler and more reliable.
