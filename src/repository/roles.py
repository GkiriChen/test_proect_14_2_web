from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import UserRole
from sqlalchemy.future import select


async def create_role(id: int, name: str, db: AsyncSession) -> UserRole:
    """
    Create a new user role in the database.

    :param id: The unique identifier for the role.
    :type id: int
    :param name: The name of the role.
    :type name: str
    :param db: The database session.
    :type db: AsyncSession
    :return: The newly created user role.
    :rtype: UserRole
    """
    role = UserRole(id=id, role_name=name)

    try:
        db.add(role)
        await db.commit()
        await db.refresh(role)
        return role
    except Exception as e:
        await db.rollback()
        raise e


async def get_role(id: int, db: AsyncSession) -> UserRole:
    """
    Retrieve a user role by its unique identifier from the database.

    :param id: The unique identifier of the user role.
    :type id: int
    :param db: The database session.
    :type db: AsyncSession
    :return: The user role with the specified ID, or None if not found.
    :rtype: UserRole | None
    """
    statement = select(UserRole).where(UserRole.id == id)
    result = await db.execute(statement)
    return result.scalars().first()


async def update_role(id: int, name: str, db: AsyncSession) -> UserRole:
    """
    Update the name of a user role in the database.

    :param id: The unique identifier of the user role to update.
    :type id: int
    :param name: The new name for the user role.
    :type name: str
    :param db: The database session.
    :type db: AsyncSession
    :return: The updated user role, or None if the role with the specified ID is not found.
    :rtype: UserRole | None
    """
    role = await get_role(id, db)
    if role:
        role.role_name = name
        await db.commit()
        return role
    else:
        return None
