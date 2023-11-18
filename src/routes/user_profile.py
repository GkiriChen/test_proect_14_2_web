from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks, Request, Form
from sqlalchemy.ext.asyncio import AsyncSession

import cloudinary
import cloudinary.uploader

from src.repository import users as repository_users
from src.repository import roles as repository_roles
from src.schemas import UserDb, UpdateUserProfileModel, UserBan
from src.services.auth import auth_service
from src.services.auth_admin import is_admin
from src.database.db import get_db
from src.database.models import User
from src.conf.config import settings
from src.services.email import send_email


profile_router = APIRouter(prefix="/profile", tags=["profile"])


@profile_router.get("/{username}", response_model=UserDb)
async def get_user_profile(username: str, db: AsyncSession = Depends(get_db)):
    """
    Get the profile information for a user by their unique username.

    :param username: The username of the user.
    :type username: str
    :param db: Database session.
    :type db: AsyncSession
    :return: User profile information.
    :rtype: UserDb
    """
    user = await repository_users.get_user_by_username(username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@profile_router.get("/me/", response_model=UserDb)
async def get_own_profile(current_user: User = Depends(auth_service.get_current_user)):
    """
    Get the profile information for the currently authenticated user.

    :param current_user: The currently authenticated user.
    :type current_user: UserDb
    :return: User profile information.
    :rtype: UserDb
    """
    return current_user


@profile_router.put("/me/", response_model=UserDb)
async def update_own_profile(user_data: UpdateUserProfileModel,
                             background_tasks: BackgroundTasks,
                             request: Request,
                             current_user: User = Depends(
                                 auth_service.get_current_user),
                             db: AsyncSession = Depends(get_db)):
    """
    Update the profile information for the currently authenticated user.

    :param user_data: Updated user information.
    :type user_data: UpdateUserProfileModel
    :param background_tasks: Background tasks to be executed after the request is processed.
    :type background_tasks: BackgroundTasks
    :param request: The HTTP request being processed.
    :type request: Request
    :param current_user: The currently authenticated user.
    :type current_user: UserDb
    :param db: Database session.
    :type db: AsyncSession
    :return: Updated user profile information.
    :rtype: UserDb
    """
    new_email = user_data.email and current_user.email != user_data.email
    if not user_data.email:
        user_data.email = current_user.email
    if user_data.password:
        user_data.password = auth_service.get_password_hash(user_data.password)

    user = await repository_users.update_user_profile(current_user.email, user_data, db)

    if new_email:
        background_tasks.add_task(
            send_email, user.email, user.username, request.base_url)
        return {"user": user, "detail": "User successfully updated. Check your email for confirmation."}
    return user


@profile_router.patch('/avatar', response_model=UserDb)
async def update_user_avatar(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: AsyncSession = Depends(get_db)):
    """
    Update the avatar for the current user.

    :param file: The image file to set as the new avatar.
    :type file: UploadFile
    :param current_user: The authenticated user.
    :type current_user: User
    :param db: Database session.
    :type db: AsyncSession
    :return: The user with the updated avatar.
    :rtype: UserDb
    """
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )

    r = cloudinary.uploader.upload(
        file.file, public_id=f'PhotoShare/{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'PhotoShare/{current_user.username}')\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user


@profile_router.put("/role", response_model=UserDb, dependencies=[Depends(is_admin)])
async def update_user_role(
    role_id: int = Form(...),
    username: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Update the role of a user.

    :param role_id: The ID of the role to assign to the user.
    :type role_id: int
    :param username: The username of the user to update.
    :type username: str
    :param current_user: The currently authenticated user.
    :type current_user: User
    :param db: The database session.
    :type db: AsyncSession
    :return: The updated user with the new role.
    :rtype: UserDb
    """

    role = await repository_roles.get_role(role_id, db)

    if role:
        user = await repository_users.update_user_role(username, role_id, db)
        if user:
            return user
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User is not found")
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role is not found")


@profile_router.put("/ban", response_model=UserBan, dependencies=[Depends(is_admin)])
async def update_user_ban(
    username: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Update the ban status of a user.

    :param username: The username of the user to update.
    :type username: str
    :param current_user: The currently authenticated user.
    :type current_user: User
    :param db: The database session.
    :type db: AsyncSession
    :return: The updated user with the new ban status.
    :rtype: UserBan
    """

    user = await repository_users.update_user_ban(username, db)
    if user:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User is not found")
