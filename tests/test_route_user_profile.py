from src.services.auth import auth_service


async def test_get_user_profile(client):
    """
    Test fetching a user profile with an invalid username.

    Parameters:
    - client: TestClient - FastAPI test client.

    The test checks if attempting to get a user profile with an invalid username returns a 404 status code.
    """
    response = client.get("/profile/testuser")
    assert response.status_code == 404


async def test_get_own_profile(client):
    """
    Test fetching the user's own profile with an invalid username.

    Parameters:
    - client: TestClient - FastAPI test client.

    The test checks if attempting to get the user's own profile with an invalid username returns a 404 status code.
    """
    access_token = auth_service.create_access_token(data={"sub": "testuser"})
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/profile/me", headers=headers)
    assert response.status_code == 404


async def test_update_own_profile(client):
    """
    Test updating the user's own profile with an invalid username.

    Parameters:
    - client: TestClient - FastAPI test client.

    The test checks if attempting to update the user's own profile with an invalid username returns a 404 status code.
    """
    access_token = auth_service.create_access_token(data={"sub": "testuser"})
    headers = {"Authorization": f"Bearer {access_token}"}
    update_data = {"username": "new_username",
                   "first_name": "New", "last_name": "User"}
    response = client.put("/profile/me", headers=headers, json=update_data)
    assert response.status_code == 404


async def test_update_user_avatar(client):
    """
    Test updating the user's avatar with an invalid username.

    Parameters:
    - client: TestClient - FastAPI test client.

    The test checks if attempting to update the user's avatar with an invalid username returns a 404 status code.
    """
    access_token = auth_service.create_access_token(data={"sub": "testuser"})
    headers = {"Authorization": f"Bearer {access_token}"}
    files = {"file": ("test_avatar.jpg", open("test_avatar.jpg", "rb"))}
    response = client.patch("/profile/avatar", headers=headers, files=files)
    assert response.status_code == 404


async def test_update_password(client):
    """
    Test updating the user's password with an invalid username.

    Parameters:
    - client: TestClient - FastAPI test client.

    The test checks if attempting to update the user's password with an invalid username returns a 404 status code.
    """
    access_token = auth_service.create_access_token(data={"sub": "testuser"})
    headers = {"Authorization": f"Bearer {access_token}"}
    update_data = {"new_password": "new_password",
                   "confirm_password": "new_password"}
    response = client.patch("/profile/update-password",
                            headers=headers, json=update_data)
    assert response.status_code == 404


async def test_update_email(client):
    """
    Test updating the user's email with an invalid username.

    Parameters:
    - client: TestClient - FastAPI test client.

    The test checks if attempting to update the user's email with an invalid username returns a 404 status code.
    """
    access_token = auth_service.create_access_token(data={"sub": "testuser"})
    headers = {"Authorization": f"Bearer {access_token}"}
    update_data = {"new_email": "new_email@example.com"}
    response = client.patch("/profile/update-email",
                            headers=headers, json=update_data)
    assert response.status_code == 404


async def test_update_user_role(client):
    """
    Test updating the user's role with an invalid username.

    Parameters:
    - client: TestClient - FastAPI test client.

    The test checks if attempting to update the user's role with an invalid username returns a 404 status code.
    """
    access_token = auth_service.create_access_token(data={"sub": "admin"})
    headers = {"Authorization": f"Bearer {access_token}"}
    update_data = {"role_id": 1, "username": "testuser"}
    response = client.put("/profile/role", headers=headers, data=update_data)
    assert response.status_code == 404
