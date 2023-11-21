from fastapi import HTTPException, status
from src.services.auth import auth_service
from src.database.models import User
from src.services.auth_admin import is_admin, is_moderator
import pytest
from unittest.mock import AsyncMock


@pytest.fixture
def mock_get_current_user():
    return AsyncMock()


def test_is_admin_success():
    user_with_admin_role = User(role_id=1)

    result = is_admin(current_user=user_with_admin_role)

    assert result == user_with_admin_role


def test_is_admin_failure():
    user_without_admin_role = User(role_id=2)

    with pytest.raises(HTTPException) as exc_info:
        is_admin(current_user=user_without_admin_role)
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN


def test_is_moderator_success():
    user_with_moderator_role = User(role_id=2)

    result = is_moderator(current_user=user_with_moderator_role)

    assert result == user_with_moderator_role


def test_is_moderator_failure():
    user_without_moderator_role = User(role_id=3)

    with pytest.raises(HTTPException) as exc_info:
        is_moderator(current_user=user_without_moderator_role)
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
