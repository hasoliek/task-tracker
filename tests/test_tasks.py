from fastapi.testclient import TestClient
import pytest


def test_create_task_valid_returns_201_with_full_body(client: TestClient):
    # Arrange
    payload = {
        "title": "Write tests",
        "description": "cover API behavior",
        "status": "ToDo",
        "priority": "High",
        "assignee": "hassan",
    }

    # Act
    response = client.post("/tasks", json=payload)

    # Assert
    assert response.status_code == 201
    data = response.json()

    assert set(data.keys()) == {
        "id",
        "title",
        "description",
        "status",
        "priority",
        "assignee",
        "due_date",
        "tags",
        "created_at",
        "updated_at",
    }

    assert isinstance(data["id"], str) and data["id"]
    assert data["title"] == "Write tests"
    assert data["description"] == "cover API behavior"
    assert data["status"] == "ToDo"
    assert data["priority"] == "High"
    assert data["assignee"] == "hassan"
    assert data["due_date"] is None
    assert data["tags"] == []
    assert isinstance(data["created_at"], str) and data["created_at"]
    assert isinstance(data["updated_at"], str) and data["updated_at"]


def test_create_task_missing_title_returns_422(client: TestClient):
    # Arrange
    payload = {"description": "no title"}

    # Act
    response = client.post("/tasks", json=payload)

    # Assert
    assert response.status_code == 422


def test_create_task_blank_title_returns_422(client: TestClient):
    # Arrange
    payload = {"title": "   "}

    # Act
    response = client.post("/tasks", json=payload)

    # Assert
    assert response.status_code == 422


def test_create_task_invalid_priority_returns_422(client: TestClient):
    # Arrange
    payload = {"title": "Task", "priority": "Urgent"}

    # Act
    response = client.post("/tasks", json=payload)

    # Assert
    assert response.status_code == 422


def test_create_task_unknown_field_returns_422(client: TestClient):
    # Arrange
    payload = {"title": "Task", "unknown_field": "x"}

    # Act
    response = client.post("/tasks", json=payload)

    # Assert
    assert response.status_code == 422


def test_list_tasks_empty_returns_200_and_empty_list(client: TestClient):
    # Act
    response = client.get("/tasks")

    # Assert
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(
    client: TestClient,
):
    # Arrange
    created = client.post("/tasks", json={"title": "todo task"})
    assert created.status_code == 201

    # Act
    response = client.get("/tasks", params={"status": "Done"})

    # Assert
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(
    client: TestClient,
):
    # Arrange
    r1 = client.post(
        "/tasks",
        json={"title": "low task", "priority": "Low"},
    )
    r2 = client.post(
        "/tasks",
        json={"title": "high task", "priority": "High"},
    )
    r3 = client.post(
        "/tasks",
        json={"title": "medium task", "priority": "Medium"},
    )

    assert r1.status_code == 201
    assert r2.status_code == 201
    assert r3.status_code == 201

    # Act
    response = client.get(
        "/tasks",
        params={"priority": "High"},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "high task"
    assert data[0]["priority"] == "High"


def test_get_task_by_id_returns_task(
    client: TestClient,
    created_task: dict,
):
    # Arrange
    task_id = created_task["id"]

    # Act
    response = client.get(f"/tasks/{task_id}")

    # Assert
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "fixture task"


def test_get_task_by_id_not_found_returns_404_with_detail(
    client: TestClient,
):
    # Arrange
    task_id = "missing-id"

    # Act
    response = client.get(f"/tasks/{task_id}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Task with id {task_id} not found"
    }


def test_patch_partial_update_keeps_other_fields(
    client: TestClient,
):
    # Arrange
    create_response = client.post(
        "/tasks",
        json={
            "title": "original title",
            "description": "original desc",
            "status": "ToDo",
            "priority": "Low",
            "assignee": "sam",
        },
    )

    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Act
    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": "updated title"},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "updated title"
    assert data["description"] == "original desc"
    assert data["status"] == "ToDo"
    assert data["priority"] == "Low"
    assert data["assignee"] == "sam"
    assert data["due_date"] is None
    assert data["tags"] == []


def test_patch_not_found_returns_404(client: TestClient):
    # Arrange
    task_id = "missing-id"

    # Act
    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": "new title"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Task with id {task_id} not found"
    }


def test_patch_valid_transition_todo_to_inprogress_returns_200(
    client: TestClient,
    created_task: dict,
):
    # Arrange
    task_id = created_task["id"]

    # Act
    response = client.patch(
        f"/tasks/{task_id}",
        json={"status": "InProgress"},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_patch_invalid_transition_todo_to_done_returns_422(
    client: TestClient,
    created_task: dict,
):
    # Arrange
    task_id = created_task["id"]

    # Act
    response = client.patch(
        f"/tasks/{task_id}",
        json={"status": "Done"},
    )

    # Assert
    assert response.status_code == 422
    assert (
        "Invalid status transition from ToDo to Done"
        in response.json()["detail"]
    )


def test_patch_same_status_returns_422(
    client: TestClient,
    created_task: dict,
):
    # Arrange
    task_id = created_task["id"]

    # Act
    response = client.patch(
        f"/tasks/{task_id}",
        json={"status": "ToDo"},
    )

    # Assert
    assert response.status_code == 422
    assert (
        "Invalid status transition from ToDo to ToDo"
        in response.json()["detail"]
    )


def test_delete_existing_returns_204_no_body(
    client: TestClient,
    created_task: dict,
):
    # Arrange
    task_id = created_task["id"]

    # Act
    response = client.delete(f"/tasks/{task_id}")

    # Assert
    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_returns_404(client: TestClient):
    # Arrange
    task_id = "missing-id"

    # Act
    response = client.delete(f"/tasks/{task_id}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {
        "detail": f"Task with id {task_id} not found"
    }


def test_create_task_with_due_date_returns_due_date(
    client: TestClient,
):
    # Arrange
    payload = {
        "title": "Task with deadline",
        "due_date": "2026-08-15",
    }

    # Act
    response = client.post("/tasks", json=payload)

    # Assert
    assert response.status_code == 201
    data = response.json()

    assert data["title"] == "Task with deadline"
    assert data["due_date"] == "2026-08-15"


def test_patch_task_updates_due_date(client: TestClient):
    # Arrange
    create_response = client.post(
        "/tasks",
        json={"title": "Task without deadline"},
    )

    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Act
    response = client.patch(
        f"/tasks/{task_id}",
        json={"due_date": "2026-09-01"},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == task_id
    assert data["title"] == "Task without deadline"
    assert data["due_date"] == "2026-09-01"


def test_list_tasks_overdue_true_returns_only_overdue_tasks(
    client: TestClient,
):
    # Arrange
    overdue_response = client.post(
        "/tasks",
        json={
            "title": "Overdue task",
            "due_date": "2020-01-01",
        },
    )
    future_response = client.post(
        "/tasks",
        json={
            "title": "Future task",
            "due_date": "2099-01-01",
        },
    )

    assert overdue_response.status_code == 201
    assert future_response.status_code == 201

    # Act
    response = client.get(
        "/tasks",
        params={"overdue": "true"},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Overdue task"
    assert data[0]["due_date"] == "2020-01-01"


def test_done_task_with_past_due_date_is_not_overdue(
    client: TestClient,
):
    # Arrange
    create_response = client.post(
        "/tasks",
        json={
            "title": "Completed task",
            "due_date": "2020-01-01",
        },
    )

    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    update_response = client.patch(
        f"/tasks/{task_id}",
        json={"status": "InProgress"},
    )
    assert update_response.status_code == 200

    update_response = client.patch(
        f"/tasks/{task_id}",
        json={"status": "Done"},
    )
    assert update_response.status_code == 200

    # Act
    response = client.get(
        "/tasks",
        params={"overdue": "true"},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()

    assert all(task["id"] != task_id for task in data)


def test_create_task_with_tags_returns_cleaned_tags(
    client: TestClient,
):
    # Arrange
    payload = {
        "title": "Tagged task",
        "tags": [
            "backend",
            " urgent ",
            "backend",
        ],
    }

    # Act
    response = client.post("/tasks", json=payload)

    # Assert
    assert response.status_code == 201
    data = response.json()

    assert data["title"] == "Tagged task"
    assert data["tags"] == ["backend", "urgent"]
    
    # Act
    response = client.post("/tasks", json=payload)

    # Assert
    assert response.status_code == 201
    data = response.json()

    assert data["title"] == "Tagged task"
    assert data["tags"] == ["backend", "urgent"]


def test_create_task_without_tags_returns_empty_list(
    client: TestClient,
):
    # Arrange
    payload = {
        "title": "Task without tags",
    }

    # Act
    response = client.post("/tasks", json=payload)

    # Assert
    assert response.status_code == 201
    assert response.json()["tags"] == []


def test_create_task_tags_must_be_list(
    client: TestClient,
):
    # Arrange
    payload = {
        "title": "Invalid tags task",
        "tags": "backend, urgent",
    }

    # Act
    response = client.post("/tasks", json=payload)

    # Assert
    assert response.status_code == 422


def test_patch_task_updates_tags(client: TestClient):
    # Arrange
    create_response = client.post(
        "/tasks",
        json={
            "title": "Task to update",
            "tags": ["backend"],
        },
    )

    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Act
    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "tags": [
                "frontend",
                " testing ",
                "frontend",
            ]
        },
    )

    # Assert
    assert response.status_code == 200
    data = response.json()

    assert data["id"] == task_id
    assert data["tags"] == ["frontend", "testing"]


def test_patch_task_can_clear_tags(client: TestClient):
    # Arrange
    create_response = client.post(
        "/tasks",
        json={
            "title": "Task with tags",
            "tags": ["backend", "api"],
        },
    )

    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Act
    response = client.patch(
        f"/tasks/{task_id}",
        json={"tags": []},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["tags"] == []


def test_patch_title_keeps_existing_tags(
    client: TestClient,
):
    # Arrange
    create_response = client.post(
        "/tasks",
        json={
            "title": "Original title",
            "tags": ["backend", "api"],
        },
    )

    assert create_response.status_code == 201
    task_id = create_response.json()["id"]

    # Act
    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": "Updated title"},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Updated title"
    assert data["tags"] == ["backend", "api"]


def test_list_tasks_filter_by_tag_returns_only_matches(
    client: TestClient,
):
    # Arrange
    backend_response = client.post(
        "/tasks",
        json={
            "title": "Backend task",
            "tags": ["backend", "api"],
        },
    )
    frontend_response = client.post(
        "/tasks",
        json={
            "title": "Frontend task",
            "tags": ["frontend"],
        },
    )
    mixed_response = client.post(
        "/tasks",
        json={
            "title": "Full stack task",
            "tags": ["backend", "frontend"],
        },
    )

    assert backend_response.status_code == 201
    assert frontend_response.status_code == 201
    assert mixed_response.status_code == 201

    # Act
    response = client.get(
        "/tasks",
        params={"tag": "backend"},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2
    assert {task["title"] for task in data} == {
        "Backend task",
        "Full stack task",
    }

    assert all("backend" in task["tags"] for task in data)


def test_list_tasks_filter_by_unknown_tag_returns_empty_list(
    client: TestClient,
):
    # Arrange
    create_response = client.post(
        "/tasks",
        json={
            "title": "Backend task",
            "tags": ["backend"],
        },
    )

    assert create_response.status_code == 201

    # Act
    response = client.get(
        "/tasks",
        params={"tag": "unknown"},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_tag_filter_trims_query_whitespace(
    client: TestClient,
):
    # Arrange
    create_response = client.post(
        "/tasks",
        json={
            "title": "Backend task",
            "tags": ["backend"],
        },
    )

    assert create_response.status_code == 201

    # Act
    response = client.get(
        "/tasks",
        params={"tag": " backend "},
    )

    # Assert
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Backend task"


def test_tag_filter_combines_with_priority_filter(
    client: TestClient,
):
    # Arrange
    high_backend = client.post(
        "/tasks",
        json={
            "title": "High backend task",
            "priority": "High",
            "tags": ["backend"],
        },
    )
    low_backend = client.post(
        "/tasks",
        json={
            "title": "Low backend task",
            "priority": "Low",
            "tags": ["backend"],
        },
    )
    high_frontend = client.post(
        "/tasks",
        json={
            "title": "High frontend task",
            "priority": "High",
            "tags": ["frontend"],
        },
    )

    assert high_backend.status_code == 201
    assert low_backend.status_code == 201
    assert high_frontend.status_code == 201

    # Act
    response = client.get(
        "/tasks",
        params={
            "tag": "backend",
            "priority": "High",
        },
    )

    # Assert
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "High backend task"
    assert data[0]["priority"] == "High"
    assert data[0]["tags"] == ["backend"]


def test_create_task_rejects_null_title(client):
    payload = {
        "title": None,
        "description": "desc",
        "status": "ToDo",
        "priority": "Medium",
        "assignee": None,
        "due_date": None,
        "tags": [],
    }

    response = client.post("/tasks", json=payload)

    assert response.status_code == 422


def test_create_task_rejects_explicit_null_title(client):
    response = client.post(
        "/tasks",
        json={
            "title": None,
            "description": "test",
            "status": "ToDo",
            "priority": "High",
        },
    )

    assert response.status_code == 422


@pytest.mark.parametrize(
    "patch_payload",
    [
        {"title": None},
        {"status": None},
        {"priority": None},
    ],
)
def test_patch_task_rejects_explicit_null_required_fields(client, patch_payload):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Task for null regression",
            "description": "test",
            "status": "ToDo",
            "priority": "Medium",
        },
    )
    assert create_response.status_code in (200, 201)
    task_id = create_response.json()["id"]

    patch_response = client.patch(f"/tasks/{task_id}", json=patch_payload)

    assert patch_response.status_code == 422


def test_patch_task_allows_omitted_fields_and_preserves_existing_values(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Original title",
            "description": "test",
            "status": "ToDo",
            "priority": "Low",
        },
    )
    assert create_response.status_code in (200, 201)
    created_task = create_response.json()
    task_id = created_task["id"]

    patch_response = client.patch(
        f"/tasks/{task_id}",
        json={"priority": "High"},
    )

    assert patch_response.status_code == 200
    updated_task = patch_response.json()
    assert updated_task["priority"] == "High"
    assert updated_task["title"] == created_task["title"]
    assert updated_task["status"] == created_task["status"]