from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.repository import users as repository_users
from src.schemas import UserModel, UserResponse, TokenModel, RequestEmail, UserDb
from src.services.auth import auth_service
from src.database.db import get_db
from src.services.auth import Auth

profile_router = APIRouter(prefix='/profile', tags=["profile"])

@profile_router.get("/{username}", response_model=UserDb)
async def get_user_profile(username: str, db: Session = Depends(get_db)):
    """
    Get the profile information for a user by their unique username.

    :param username: The username of the user.
    :type username: str
    :param db: Database session.
    :type db: Session
    :return: User profile information.
    :rtype: UserDb
    """
    user = await repository_users.get_user_by_username(username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

@profile_router.get("/me", response_model=UserDb)
async def get_own_profile(current_user: UserDb = Depends(Auth.get_current_user)):
    """
    Get the profile information for the currently authenticated user.

    :param current_user: The currently authenticated user.
    :type current_user: UserDb
    :return: User profile information.
    :rtype: UserDb
    """
    return current_user

@profile_router.put("/me", response_model=UserDb)
async def update_own_profile(user_data: UserModel, current_user: UserDb = Depends(Auth.get_current_user), db: Session = Depends(get_db)):
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
    user = await repository_users.update_user(current_user.id, user_data, db)
    return user



