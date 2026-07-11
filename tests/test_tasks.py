from fastapi.testclient import TestClient


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
        "created_at",
        "updated_at",
    }
    assert isinstance(data["id"], str) and data["id"]
    assert data["title"] == "Write tests"
    assert data["description"] == "cover API behavior"
    assert data["status"] == "ToDo"
    assert data["priority"] == "High"
    assert data["assignee"] == "hassan"
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
    # Arrange

    # Act
    response = client.get("/tasks")

    # Assert
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client: TestClient):
    # Arrange
    created = client.post("/tasks", json={"title": "todo task"})
    assert created.status_code == 201

    # Act
    response = client.get("/tasks", params={"status": "Done"})

    # Assert
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(client: TestClient):
    # Arrange
    r1 = client.post("/tasks", json={"title": "low task", "priority": "Low"})
    r2 = client.post("/tasks", json={"title": "high task", "priority": "High"})
    r3 = client.post("/tasks", json={"title": "medium task", "priority": "Medium"})
    assert r1.status_code == 201
    assert r2.status_code == 201
    assert r3.status_code == 201

    # Act
    response = client.get("/tasks", params={"priority": "High"})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "high task"
    assert data[0]["priority"] == "High"


def test_get_task_by_id_returns_task(client: TestClient, created_task: dict):
    # Arrange
    task_id = created_task["id"]

    # Act
    response = client.get(f"/tasks/{task_id}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "fixture task"


def test_get_task_by_id_not_found_returns_404_with_detail(client: TestClient):
    # Arrange
    task_id = "missing-id"

    # Act
    response = client.get(f"/tasks/{task_id}")

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": f"Task with id {task_id} not found"}


def test_patch_partial_update_keeps_other_fields(client: TestClient):
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
    response = client.patch(f"/tasks/{task_id}", json={"title": "updated title"})

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "updated title"
    assert data["description"] == "original desc"
    assert data["status"] == "ToDo"
    assert data["priority"] == "Low"
    assert data["assignee"] == "sam"


def test_patch_not_found_returns_404(client: TestClient):
    # Arrange
    task_id = "missing-id"

    # Act
    response = client.patch(f"/tasks/{task_id}", json={"title": "new title"})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": f"Task with id {task_id} not found"}


def test_patch_valid_transition_todo_to_inprogress_returns_200(
    client: TestClient, created_task: dict
):
    # Arrange
    task_id = created_task["id"]

    # Act
    response = client.patch(f"/tasks/{task_id}", json={"status": "InProgress"})

    # Assert
    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_patch_invalid_transition_todo_to_done_returns_422(
    client: TestClient, created_task: dict
):
    # Arrange
    task_id = created_task["id"]

    # Act
    response = client.patch(f"/tasks/{task_id}", json={"status": "Done"})

    # Assert
    assert response.status_code == 422
    assert "Invalid status transition from ToDo to Done" in response.json()["detail"]


def test_patch_same_status_returns_422(client: TestClient, created_task: dict):
    # Arrange
    task_id = created_task["id"]

    # Act
    response = client.patch(f"/tasks/{task_id}", json={"status": "ToDo"})

    # Assert
    assert response.status_code == 422
    assert "Invalid status transition from ToDo to ToDo" in response.json()["detail"]


def test_delete_existing_returns_204_no_body(client: TestClient, created_task: dict):
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
    assert response.json() == {"detail": f"Task with id {task_id} not found"}