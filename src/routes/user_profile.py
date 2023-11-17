from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession

import cloudinary
import cloudinary.uploader

from src.repository import users as repository_users
from src.schemas import UserDb, UpdateUserProfileModel
from src.services.auth import auth_service
from src.database.db import get_db
from src.database.models import User
from src.conf.config import settings


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
async def update_own_profile(user_data: UpdateUserProfileModel, current_user: User = Depends(auth_service.get_current_user), db: AsyncSession = Depends(get_db)):
    """
    Update the profile information for the currently authenticated user.

    :param user_data: Updated user information.
    :type user_data: UserModel
    :param current_user: The currently authenticated user.
    :type current_user: UserDb
    :param db: Database session.
    :type db: Session
    :return: Updated user profile information.
    :rtype: UserDb
    """
    user = await repository_users.update_user_profile(current_user.email, user_data, db)
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
