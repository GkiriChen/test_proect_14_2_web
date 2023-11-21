import pytest
from src.database.models import UserRole
from src.repository.roles import create_role, get_role, update_role


@pytest.mark.asyncio
async def test_create_role(session):
    role = await create_role(id=1, name='Admin', db=session)
    assert isinstance(role, UserRole)
    assert role.id == 1
    assert role.role_name == 'Admin'


@pytest.mark.asyncio
async def test_get_role(session):
    role = await get_role(id=1, db=session)
    assert isinstance(role, UserRole)
    assert role.id == 1


@pytest.mark.asyncio
async def test_update_role(session):
    updated_role = await update_role(id=1, name='Moderator', db=session)
    assert isinstance(updated_role, UserRole)
    assert updated_role.role_name == 'Moderator'

    non_existent_role = await update_role(id=100, name='New Role', db=session)
    assert non_existent_role is None
