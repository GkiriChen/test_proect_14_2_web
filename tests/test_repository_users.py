import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import UpdateUserProfileModel, UserModel
from src.database.models import User
from src.repository.users import (
    get_user_by_username,  
    get_user_by_email,
    create_user, 
    update_token, 
    update_user_password, 
    update_user_email,
    confirmed_email,
    update_avatar,
    update_user_profile,
    update_user_role,
    update_user_ban,
)


@pytest.mark.asyncio
async def test_create_user(session):
    """
    Test the creation of a new user.

    This test case validates the functionality of the `create_user` function,
    which creates a new user in the database. It checks if the created user has
    the expected attributes.
    """
    user_data = UserModel(username="test_user",
                          first_name="Test",
                          last_name="Tests",
                          email="test@example.com", 
                          password="password")
    created_user = await create_user(user_data, session)
    assert isinstance(created_user, User)
    assert created_user.username == "test_user"
    assert created_user.email == "test@example.com"
    assert created_user.role_id == 1  


@pytest.mark.asyncio
async def test_get_user_by_username(session):
    """
    Test the retrieval of a user by username.

    This test case validates the functionality of the `get_user_by_username` function,
    which retrieves a user from the database by their username. It checks if the returned
    user has the expected username.
    """
    user = await get_user_by_username("test_user", session)
    assert isinstance(user, User)
    assert user.username == "test_user"


@pytest.mark.asyncio
async def test_update_token(session):
    """
    Test the update of a user's token.

    This test case validates the functionality of the `update_token` function,
    which updates a user's refresh token. It checks if the user's refresh token
    is updated to the expected value.
    """
    user = await get_user_by_username("test_user", session)
    await update_token(user, "new_token", session)
    assert user.refresh_token == "new_token"


@pytest.mark.asyncio
async def test_update_user_password(session):
    """
    Test the update of a user's password.

    This test case validates the functionality of the `update_user_password` function,
    which updates a user's password. It checks if the user's password is updated
    to the expected hashed password.
    """
    user = await get_user_by_username("test_user", session)
    await update_user_password(user, "new_hashed_password", session)
    assert user.password == "new_hashed_password"


@pytest.mark.asyncio
async def test_get_user_by_email(session):
    """
    Test the retrieval of a user by email.

    This test case validates the functionality of the `get_user_by_email` function,
    which retrieves a user from the database by their email. It checks if the returned
    user has the expected email.
    """
    user = await get_user_by_email("test@example.com", session)
    assert isinstance(user, User)
    assert user.email == "test@example.com"


@pytest.mark.asyncio
async def test_update_user_email(session):
    """
    Test the update of a user's email.

    This test case validates the functionality of the `update_user_email` function,
    which updates a user's email. It checks if the user's email is updated to the
    expected value and if the user's confirmation status is appropriately set.
    """
    user = await get_user_by_username("test_user", session)
    await update_user_email(user, "new_email@example.com", session)
    assert user.email == "new_email@example.com"
    assert not user.confirmed  


@pytest.mark.asyncio
async def test_confirmed_email(session):
    """
    Test the confirmation of a user's email.

    This test case validates the functionality of the `confirmed_email` function,
    which confirms a user's email. It checks if the user's confirmation status
    is appropriately set to True after confirmation.
    """
    await confirmed_email("new_email@example.com", session)
    user = await get_user_by_email("new_email@example.com", session)
    assert user.confirmed


@pytest.mark.asyncio
async def test_update_avatar(session):
    """
    Test the update of a user's avatar.

    This test case validates the functionality of the `update_avatar` function,
    which updates a user's avatar URL. It checks if the user's avatar URL is updated
    to the expected value.
    """
    user = await update_avatar("new_email@example.com", "new_avatar_url", session)
    assert user.avatar == "new_avatar_url"


@pytest.mark.asyncio
async def test_update_user_role(session):
    """
    Test the update of a user's role.

    This test case validates the functionality of the `update_user_role` function,
    which updates a user's role. It checks if the user's role is updated to the
    expected role ID.
    """
    user = await update_user_role("test_user", 2, session)
    assert user.role_id == 2


@pytest.mark.asyncio
async def test_update_user_ban(session):
    """
    Test the update of a user's ban status.

    This test case validates the functionality of the `update_user_ban` function,
    which updates a user's ban status. It checks if the user's ban status is
    appropriately set to True after the update.
    """
    user = await update_user_ban("test_user", session)
    assert user.ban


@pytest.mark.asyncio
async def test_update_user_profile(session):
    """
    Test the update of a user's profile.

    This test case validates the functionality of the `update_user_profile` function,
    which updates various fields of a user's profile. It checks if the user's profile
    fields are updated to the expected values.
    """
    user = await update_user_profile("new_email@example.com", UpdateUserProfileModel(username="", first_name="", last_name="new_username"), session)
    assert user.last_name == "new_username"
