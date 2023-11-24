from fastapi import HTTPException, status
from src.services.auth import auth_service
from src.database.models import User
from src.services.auth_admin import is_admin, is_moderator
import pytest
from unittest.mock import AsyncMock


@pytest.fixture
def mock_get_current_user():
    """
    Fixture function to provide a mock implementation of the `get_current_user` function.

    Returns:
    - AsyncMock: Mock object for `get_current_user`.
    """
    return AsyncMock()


def test_is_admin_success():
    """
    Test the `is_admin` function for a user with an admin role.

    The function should return the user if they have an admin role.

    Raises:
    - AssertionError: If the result is not as expected.
    """
    user_with_admin_role = User(role_id=1)

    result = is_admin(current_user=user_with_admin_role)

    assert result == user_with_admin_role


def test_is_admin_failure():
    """
    Test the `is_admin` function for a user without an admin role.

    The function should raise an HTTPException with a 403 status code.

    Raises:
    - HTTPException: If the user does not have an admin role.
    - AssertionError: If the HTTPException status code is not 403.
    """
    user_without_admin_role = User(role_id=2)

    with pytest.raises(HTTPException) as exc_info:
        is_admin(current_user=user_without_admin_role)
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN


def test_is_moderator_success():
    """
    Test the `is_moderator` function for a user with a moderator role.

    The function should return the user if they have a moderator role.

    Raises:
    - AssertionError: If the result is not as expected.
    """
    user_with_moderator_role = User(role_id=2)

    result = is_moderator(current_user=user_with_moderator_role)

    assert result == user_with_moderator_role


def test_is_moderator_failure():
    """
    Test the `is_moderator` function for a user without a moderator role.

    The function should raise an HTTPException with a 403 status code.

    Raises:
    - HTTPException: If the user does not have a moderator role.
    - AssertionError: If the HTTPException status code is not 403.
    """
    user_without_moderator_role = User(role_id=3)

    with pytest.raises(HTTPException) as exc_info:
        is_moderator(current_user=user_without_moderator_role)
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
