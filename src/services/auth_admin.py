from fastapi import Depends, HTTPException, status
from src.services.auth import auth_service
from src.database.models import User


def is_admin(current_user: User = Depends(auth_service.get_current_user)):
    """
    Check if the current user has administrator privileges.

    :param current_user: The currently authenticated user.
    :type current_user: User
    :raises HTTPException: Raises a 403 Forbidden HTTP exception if the user does not have administrator status.
    :return: The authenticated user if they have administrator privileges.
    :rtype: User
    """
    if current_user.role_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied. You do not have administrator status."
        )
    return current_user


def is_moderator(current_user: User = Depends(auth_service.get_current_user)):
    """
    Check if the current user has moderator privileges.

    :param current_user: The currently authenticated user.
    :type current_user: User
    :raises HTTPException: Raises a 403 Forbidden HTTP exception if the user does not have moderator status.
    :return: The authenticated user if they have moderator privileges.
    :rtype: User
    """
    if current_user.role_id != 1 and current_user.role_id != 2:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied. You do not have moderator status."
        )
    return current_user

def is_user(current_user: User = Depends(auth_service.get_current_user)):
    """
    Check if the current user has moderator privileges.

    :param current_user: The currently authenticated user.
    :type current_user: User
    :raises HTTPException: Raises a 403 Forbidden HTTP exception if the user does not have moderator status.
    :return: The authenticated user if they have moderator privileges.
    :rtype: User
    """
    return current_user