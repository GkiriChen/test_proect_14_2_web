from libgravatar import Gravatar
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from src.database.models import User, UserRole
from src.schemas import UserModel
from sqlalchemy.ext.asyncio import AsyncSession


async def get_user_by_email(email: str, db: AsyncSession) -> User:
    """
    Retrieves a user by their email from the database.

    :param email: The email address of the user to retrieve.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: The user with the specified email, or None if not found.
    :rtype: User | None
    """
    try:
        result = await  db.execute(select(User).filter(User.email == email))
        user = result.scalar_one_or_none()
        return user

    except NoResultFound:
        return None


async def create_user(body: UserModel, db: AsyncSession) -> User:
    """
    Creates a new user in the database.

    :param body: The data for the user to create.
    :type body: UserModel
    :param db: The database session.
    :type db: Session
    :return: The newly created user.
    :rtype: User
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        raise e
    new_user = User(**body.dict(), avatar=avatar)

    # Проверка наличия роли 'user' в базе данных
    user_role = await db.execute(select(UserRole).where(UserRole.role_name == 'user'))
    user_role = await user_role.scalar_one_or_none()

    # Если роль 'user' не существует, создаем ее
    if not user_role:
        user_role = UserRole(role_name='user')
        db.add(user_role)
        await db.commit()
        await db.refresh(user_role)

    # Присвоение role_id новому пользователю
    new_user.role_id = user_role.id

    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except Exception as e:
        await db.rollback()
        raise e


async def update_token(user: User, token: str | None, db: AsyncSession) -> None:
    """
    Updates the refresh token for a user in the database.

    :param user: The user whose token should be updated.
    :type user: User
    :param token: The new refresh token or None to remove the token.
    :type token: str | None
    :param db: The database session.
    :type db: Session
    :return: None
    """
    user.refresh_token = token
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e


async def confirmed_email(email: str, db: AsyncSession) -> None:
    """
    Marks a user's email as confirmed in the database.

    :param email: The email address of the user to mark as confirmed.
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e


async def update_avatar(email, url: str, db: AsyncSession) -> User:
    """
    Updates the avatar URL for a user in the database.

    :param email: The email address of the user to update.
    :type email: str
    :param url: The new avatar URL for the user.
    :type url: str
    :param db: The database session.
    :type db: Session
    :return: The user with the updated avatar URL.
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    try:
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e


from typing import Optional
from src.schemas import UpdateUserProfileModel


async def update_user_profile(email: str, profile_data: UpdateUserProfileModel, db: AsyncSession) -> User:
    """
    Updates the profile information for a user in the database.

    :param email: The email address of the user to update.
    :type email: str
    :param profile_data: The updated profile information.
    :type profile_data: UpdateUserProfileModel
    :param db: The database session.
    :type db: Session
    :return: The user with the updated profile information.
    :rtype: User
    """
    user = await get_user_by_email(email, db)

    if profile_data.avatar:
        user.avatar = profile_data.avatar

    if profile_data.username:
        user.username = profile_data.username

    if profile_data.email:
        user.email = profile_data.email

    try:
        async with db.begin():
            await db.commit()
            await db.refresh(user)
    except Exception as e:
        await db.rollback()
        raise e

    return user
