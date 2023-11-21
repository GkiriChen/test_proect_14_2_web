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
    user = await get_user_by_username("test_user", session)
    assert isinstance(user, User)
    assert user.username == "test_user"


@pytest.mark.asyncio
async def test_update_token(session):
    user = await get_user_by_username("test_user", session)
    await update_token(user, "new_token", session)
    assert user.refresh_token == "new_token"


@pytest.mark.asyncio
async def test_update_user_password(session):
    user = await get_user_by_username("test_user", session)
    await update_user_password(user, "new_hashed_password", session)
    assert user.password == "new_hashed_password"


@pytest.mark.asyncio
async def test_get_user_by_email(session):
    user = await get_user_by_email("test@example.com", session)
    assert isinstance(user, User)
    assert user.email == "test@example.com"


@pytest.mark.asyncio
async def test_update_user_email(session):
    user = await get_user_by_username("test_user", session)
    await update_user_email(user, "new_email@example.com", session)
    assert user.email == "new_email@example.com"
    assert not user.confirmed  


@pytest.mark.asyncio
async def test_confirmed_email(session):
    await confirmed_email("new_email@example.com", session)
    user = await get_user_by_email("new_email@example.com", session)
    assert user.confirmed


@pytest.mark.asyncio
async def test_update_avatar(session):
    user = await update_avatar("new_email@example.com", "new_avatar_url", session)
    assert user.avatar == "new_avatar_url"


@pytest.mark.asyncio
async def test_update_user_role(session):
    user = await update_user_role("test_user", 2, session)
    assert user.role_id == 2


@pytest.mark.asyncio
async def test_update_user_ban(session):
    user = await update_user_ban("test_user", session)
    assert user.ban


@pytest.mark.asyncio
async def test_update_user_profile(session):
    user = await update_user_profile("new_email@example.com", UpdateUserProfileModel(username="", first_name="", last_name="new_username"), session)
    assert user.last_name == "new_username"
