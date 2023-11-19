from src.schemas import UpdateUserProfileModel
from libgravatar import Gravatar
from src.database.models import User
from src.schemas import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def get_user_by_username(username: str, db: AsyncSession) -> User:
    """
    Retrieves a user by their username from the database.

    :param username: The username of the user to retrieve.
    :type username: str
    :param db: The database session.
    :type db: AsyncSession
    :return: The user with the specified email, or None if not found.
    :rtype: User | None
    """
    statement = select(User).where(User.username == username)
    result = await db.execute(statement)
    return result.scalars().first()


async def get_user_by_email(email: str, db: AsyncSession) -> User:
    """
    Retrieves a user by their email from the database.

    :param email: The email address of the user to retrieve.
    :type email: str
    :param db: The database session.
    :type db: AsyncSession
    :return: The user with the specified email, or None if not found.
    :rtype: User | None
    """
    statement = select(User).where(User.email == email)
    result = await db.execute(statement)
    return result.scalars().first()


async def create_user(body: UserModel, db: AsyncSession) -> User:
    """
    Creates a new user in the database.

    :param body: The data for the user to create.
    :type body: UserModel
    :param db: The database session.
    :type db: AsyncSession
    :return: The newly created user.
    :rtype: User
    """
    result = await db.execute(select(User).limit(1))
    existing_user = result.scalar()

    if existing_user is None:   # First user is an admin
        role_id = 1
    else:
        role_id = 3

    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)

    new_user = User(**body.dict(), role_id=role_id, avatar=avatar)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: AsyncSession) -> None:
    """
    Updates the refresh token for a user in the database.

    :param user: The user whose token should be updated.
    :type user: User
    :param token: The new refresh token or None to remove the token.
    :type token: str | None
    :param db: The database session.
    :type db: AsyncSession
    :return: None
    """
    user.refresh_token = token
    await db.commit()


async def update_user_password(user: User, hashed_password: str, db: AsyncSession):
    """
    Update the user's password in the database.

    :param user: The user whose password needs to be updated.
    :type user: User
    :param hashed_password: The hashed new password.
    :type hashed_password: str
    :param db: Database session.
    :type db: AsyncSession
    """
    user.password = hashed_password
    await db.commit()
    await db.refresh(user)


async def update_user_email(user: User, new_email: str, db: AsyncSession):
    """
    Update the user's email in the database.

    :param user: The user to update.
    :type user: User
    :param new_email: The new email for the user.
    :type new_email: str
    :param db: Database session.
    :type db: AsyncSession
    """
    user.email = new_email
    user.confirmed = False

    await db.commit()


async def confirmed_email(email: str, db: AsyncSession) -> None:
    """
    Marks a user's email as confirmed in the database.

    :param email: The email address of the user to mark as confirmed.
    :type email: str
    :param db: The database session.
    :type db: AsyncSession
    :return: None
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()


async def update_avatar(email, url: str, db: AsyncSession) -> User:
    """
    Updates the avatar URL for a user in the database.

    :param email: The email address of the user to update.
    :type email: str
    :param url: The new avatar URL for the user.
    :type url: str
    :param db: The database session.
    :type db: AsyncSession
    :return: The user with the updated avatar URL.
    :rtype: User
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    return user


async def update_user_profile(email: str, profile_data: UpdateUserProfileModel, db: AsyncSession) -> User:
    """
    Updates the profile information for a user in the database.

    :param email: The email address of the user to update.
    :type email: str
    :param profile_data: The updated profile information.
    :type profile_data: UpdateUserProfileModel
    :param db: The database session.
    :type db: AsyncSession
    :return: The user with the updated profile information.
    :rtype: User
    """
    user = await get_user_by_email(email, db)

    if profile_data.username:
        user.username = profile_data.username

    if profile_data.first_name:
        user.first_name = profile_data.first_name

    if profile_data.last_name:
        user.last_name = profile_data.last_name

    await db.commit()

    return user


async def update_user_role(username: str, role_id: int, db: AsyncSession) -> User:
    """
    Update the role of a user in the database.

    :param username: The username of the user to update.
    :type username: str
    :param role_id: The new role ID for the user.
    :type role_id: int
    :param db: The database session.
    :type db: AsyncSession
    :return: The user with the updated role information.
    :rtype: User
    """
    user = await get_user_by_username(username, db)
    if user:
        user.role_id = role_id
        await db.commit()

    return user


async def update_user_ban(username: str, db: AsyncSession) -> User:
    """
    Toggle the ban status of a user in the database.

    :param username: The username of the user to update.
    :type username: str
    :param db: The database session.
    :type db: AsyncSession
    :return: The user with the updated ban status.
    :rtype: User
    """
    user = await get_user_by_username(username, db)
    if user:
        user.ban = not user.ban
        await db.commit()

    return user
