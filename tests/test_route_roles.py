from src.services.auth import auth_service


def test_create_role_unauthorized(client):
    """
    Test creating a role with unauthorized access.

    Parameters:
    - client: TestClient - FastAPI test client.

    The test checks if attempting to create a role without proper authorization results in the expected unauthorized response.
    """
    role_data = {"id": 2, "role_name": "Moderator"}
    response = client.post("/api/roles/create", data=role_data)
    assert response.status_code == 401


def test_update_role_unauthorized(client):
    """
    Test updating a role with unauthorized access.

    Parameters:
    - client: TestClient - FastAPI test client.

    The test first creates a role, then checks if attempting to update the role without proper authorization
    results in the expected unauthorized response.
    """
    role_data = {"id": 3, "role_name": "User"}
    client.post("/api/roles/create", data=role_data)
    updated_role_data = {"id": 3, "role_name": "Updated User"}

    response = client.put("/api/roles/update", data=updated_role_data)

    assert response.status_code == 401
