import pytest
from src.database.models import UserRole
from src.repository.roles import create_role, get_role, update_role


@pytest.mark.asyncio
async def test_create_role(session):
    """
    Test the create_role function.

    Parameters:
    - session: AsyncSession - An async database session.

    The test checks if the create_role function correctly creates a UserRole instance with the specified parameters.
    """
    role = await create_role(id=1, name='Admin', db=session)
    assert isinstance(role, UserRole)
    assert role.id == 1
    assert role.role_name == 'Admin'


@pytest.mark.asyncio
async def test_get_role(session):
    """
    Test the get_role function.

    Parameters:
    - session: AsyncSession - An async database session.

    The test checks if the get_role function correctly retrieves a UserRole instance with the specified ID.
    """
    role = await get_role(id=1, db=session)
    assert isinstance(role, UserRole)
    assert role.id == 1


@pytest.mark.asyncio
async def test_update_role(session):
    """
    Test the update_role function.

    Parameters:
    - session: AsyncSession - An async database session.

    The test checks if the update_role function correctly updates the role_name of a UserRole instance with the specified ID.
    It also checks if the function returns None when trying to update a non-existent role.
    """
    updated_role = await update_role(id=1, name='Moderator', db=session)
    assert isinstance(updated_role, UserRole)
    assert updated_role.role_name == 'Moderator'

    non_existent_role = await update_role(id=100, name='New Role', db=session)
    assert non_existent_role is None
