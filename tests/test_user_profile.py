import unittest
import tracemalloc
import asyncio
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import UserDb, UpdateUserProfileModel
from src.routes.user_profile import profile_router
from src.database.models import User
from src.services.auth import auth_service
from src.conf.config import settings
from datetime import datetime

tracemalloc.start()

class TestProfileRouter(unittest.TestCase):

    def setUp(self) -> None:
        self.session = AsyncMock(spec=AsyncSession())

    def tearDown(self) -> None:
        del self.session

    async def test_get_user_profile(self):
        mock_user = UserDb(
            id=1,
            role_id=1,
            first_name="John",
            last_name="Doe",
            created_at=datetime.utcnow(),
            avatar="path/to/avatar",
            username="testuser",
            email="test@example.com",
        )
        mock_db = AsyncMock(spec=AsyncSession())
        mock_db.execute.return_value.scalars().first.return_value = mock_user

        with patch("src.repository.users.get_user_by_username", return_value=mock_user):
            response = await self.client.get("/profile/testuser")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), mock_user.dict())

    async def test_get_nonexistent_user_profile(self):
        with patch("src.repository.users.get_user_by_username", return_value=None):
            response = await self.client.get("/profile/nonexistentuser")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "User not found"})

    async def test_get_own_profile_unauthorized(self):
        with patch("src.services.auth_service.get_current_user", return_value=None):
            response = await self.client.get("/profile/me/")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Not authenticated"})

    async def test_update_own_profile_invalid_data(self):
        mock_update_data = UpdateUserProfileModel(username="newusername")
        with patch("src.services.auth_service.get_current_user", return_value=None):
            response = await self.client.put("/profile/me/", json=mock_update_data.dict())

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"detail": "Not authenticated"})

    async def test_update_user_avatar_invalid_file(self):
        with patch("cloudinary.uploader.upload", side_effect=Exception("Invalid file")), \
             patch("src.repository.users.update_avatar", return_value=None):
            response = await self.client.patch("/profile/avatar", files={"file": ("test.txt", b"invalidfile")})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Invalid file format"})

    async def test_update_password_invalid_token(self):
        mock_new_password_data = {"new_password": "newpass", "confirm_password": "newpass", "token": "invalidtoken"}
        with patch("src.services.auth_service.get_email_from_token", side_effect=Exception("Invalid token")):
            response = await self.client.patch("/profile/update-password", json=mock_new_password_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"detail": "Invalid token"})

    async def test_update_email_user_not_found(self):
        mock_new_email_data = {"new_email": "newemail@example.com", "token": "mocktoken"}
        with patch("src.services.auth_service.get_email_from_token", return_value="test@example.com"), \
             patch("src.repository.users.get_user_by_email", return_value=None):
            response = await self.client.patch("/profile/update-email", json=mock_new_email_data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "User not found"})

    async def test_update_user_role_invalid_role(self):
        mock_role_data = {"role_id": 99, "username": "testuser"}
        with patch("src.repository.roles.get_role", return_value=None):
            response = await self.client.put("/profile/role", data=mock_role_data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Role not found"})

if __name__ == "__main__":
    asyncio.run(unittest.main())