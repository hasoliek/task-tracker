Mini Architecture Decision Record (Mini-ADR)

Title

Due Dates, Overdue Filtering, and Tags for the Task Tracker

Status

Proposed – To be implemented as part of the Mid-Course Project.

Context

The existing FastAPI Task Tracker application already supports task creation, retrieval, updating, deletion, status transitions, priority filtering, and a Kanban-style frontend.

The Mid-Course Project extends the application with two new features:

1. Due Dates and Overdue Filtering
2. Tags / Labels and Tag Filtering

The implementation should remain lightweight and consistent with the current architecture. The project currently uses Pydantic models for validation, FastAPI endpoints for API requests, business rules for reusable logic, in-memory storage for task management, and a single-page frontend that communicates with the backend.

The project does not require authentication, persistent database storage, notifications, scheduled background jobs, or additional architectural layers.

⸻

Decision 1: Represent Due Dates as Optional Calendar Dates

An optional due_date field will be added to the task models using Python’s date type.

The field will be included in:

* TaskCreate
* TaskUpdate
* TaskResponse

FastAPI and Pydantic will validate dates using the ISO format (YYYY-MM-DD).

A task may be created without a due date.

For PATCH requests:

* If due_date is omitted, the existing value remains unchanged.
* If a valid date is provided, it replaces the existing value.
* If null is provided, the due date is removed.

Reason

Using a calendar date is sufficient because the feature only requires daily deadlines. Time-of-day and timezone support are unnecessary for this project.

Alternatives Considered

Store the due date as a string

Rejected because string values require manual parsing and validation.

Use a datetime value

Rejected because time and timezone handling would increase complexity without providing additional value for the project requirements.

⸻

Decision 2: Calculate Overdue Status Dynamically

The application will not store an overdue field.

Instead, overdue status will be calculated whenever tasks are retrieved or filtered.

A task is overdue when:

* it has a due date before the current date, and
* its status is not Done.

The following tasks are never considered overdue:

* tasks without a due date,
* tasks due today,
* tasks with future due dates,
* completed tasks.

The overdue calculation will be implemented as a reusable helper function in business_rules.py.

The existing GET /tasks endpoint will be extended with an optional Boolean query parameter:

GET /tasks?overdue=true

When enabled, only overdue tasks will be returned.

Reason

Overdue status changes automatically as time passes. Calculating it dynamically avoids stale data and removes the need for scheduled updates or background jobs.

Alternatives Considered

Store an overdue Boolean field inside each task

Rejected because the value would become incorrect whenever the current date changes or the task status is updated.

Create a separate endpoint for overdue tasks

Rejected because overdue is simply another filtering criterion and fits naturally within the existing task listing endpoint.

⸻

Decision 3: Represent Tags as a List of Strings

The task models will include a tags field represented as a list of strings.

Tags will:

* be optional during task creation,
* be validated individually,
* reject blank values after trimming whitespace,
* return an empty list when no tags are assigned.

During PATCH requests:

* providing a new tag list replaces the existing tags,
* providing an empty list removes all tags,
* omitting the field preserves the current tags.

Reason

Representing tags as a list aligns naturally with JSON, simplifies validation, supports exact filtering, and makes updates easier than storing comma-separated text.

Alternatives Considered

Store tags as a comma-separated string

Rejected because parsing, validation, updating individual tags, and filtering become unnecessarily complicated.

Create separate Tag models and CRUD endpoints

Rejected because introducing additional entities would significantly increase the scope of a small in-memory project.

⸻

Decision 4: Add Tag Filtering to the Existing Task Endpoint

The existing GET /tasks endpoint will support an optional tag query parameter.

Example:

GET /tasks?tag=backend

Filtering will use exact tag matching. A task matches only if it contains the complete requested tag.

Partial text matching will not be supported.

Tag filtering will work alongside the existing status, priority, and overdue filters.

Reason

Extending the existing endpoint maintains a simple API and avoids duplicating functionality.

Alternatives Considered

Support partial text matching

Rejected because it may produce unexpected results and make filtering less predictable.

Create a separate tag-specific endpoint

Rejected because filtering belongs within the existing task retrieval endpoint.

⸻

Decision 5: Extend the Existing Frontend

The existing single-page frontend will be enhanced rather than redesigned.

The following interface elements will be added:

* an optional due date input,
* a tags input,
* due date display on task cards,
* an overdue visual indicator,
* an overdue filter control,
* tag labels displayed on task cards,
* a tag filter control.

The current modal dialog, task card rendering logic, API requests, and Kanban board structure will all be reused.

Reason

The current frontend already supports creating, editing, displaying, and filtering tasks. Extending these components minimizes implementation effort while keeping the application consistent.

Alternatives Considered

Rewrite the frontend using a JavaScript framework

Rejected because it would unnecessarily increase project complexity.

Implement backend support only

Rejected because both selected features benefit from visible frontend functionality, and the project requires feature implementation across the application.

⸻

Consequences

Positive

* The implementation remains consistent with the existing architecture.
* Pydantic provides automatic validation for dates and tags.
* Overdue status always reflects the current date.
* Existing PATCH behavior naturally supports optional fields.
* Filtering remains centralized within the existing task endpoint.
* No new architectural layers or external dependencies are introduced.

Trade-offs

* Tags are simple strings without additional metadata such as colors or descriptions.
* Tag filtering supports exact matches only.
* Date calculations rely on the server’s current date.
* Task data remains in memory and is lost when the application restarts.
* Updating tags replaces the complete tag list rather than supporting individual add/remove operations.

⸻

Implementation Scope

The following project files are expected to change:

* app/models.py
* app/business_rules.py
* app/storage.py
* app/main.py
* frontend/index.html
* tests/test_tasks.py
* README.md

