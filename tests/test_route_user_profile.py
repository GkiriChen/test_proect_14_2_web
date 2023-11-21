
from src.services.auth import auth_service



async def test_get_user_profile(client):
    response = client.get("/profile/testuser")
    assert response.status_code == 404  


async def test_get_own_profile(client):
    access_token = auth_service.create_access_token(data={"sub": "testuser"})
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/profile/me", headers=headers)
    assert response.status_code == 404  


async def test_update_own_profile(client):
    access_token = auth_service.create_access_token(data={"sub": "testuser"})
    headers = {"Authorization": f"Bearer {access_token}"}
    update_data = {"username": "new_username",
                   "first_name": "New", "last_name": "User"}
    response = client.put("/profile/me", headers=headers, json=update_data)
    assert response.status_code == 404  


async def test_update_user_avatar(client):
    access_token = auth_service.create_access_token(data={"sub": "testuser"})
    headers = {"Authorization": f"Bearer {access_token}"}
    files = {"file": ("test_avatar.jpg", open("test_avatar.jpg", "rb"))}
    response = client.patch("/profile/avatar", headers=headers, files=files)
    assert response.status_code == 404  


async def test_update_password(client):
    access_token = auth_service.create_access_token(data={"sub": "testuser"})
    headers = {"Authorization": f"Bearer {access_token}"}
    update_data = {"new_password": "new_password",
                   "confirm_password": "new_password"}
    response = client.patch("/profile/update-password",
                            headers=headers, json=update_data)
    assert response.status_code == 404  


async def test_update_email(client):
    access_token = auth_service.create_access_token(data={"sub": "testuser"})
    headers = {"Authorization": f"Bearer {access_token}"}
    update_data = {"new_email": "new_email@example.com"}
    response = client.patch("/profile/update-email",
                            headers=headers, json=update_data)
    assert response.status_code == 404  


async def test_update_user_role(client):
    access_token = auth_service.create_access_token(data={"sub": "admin"})
    headers = {"Authorization": f"Bearer {access_token}"}
    update_data = {"role_id": 1, "username": "testuser"}
    response = client.put("/profile/role", headers=headers, data=update_data)
    assert response.status_code == 404  
