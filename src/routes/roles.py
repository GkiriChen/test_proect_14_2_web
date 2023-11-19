from fastapi import APIRouter, HTTPException, Depends, status, Form
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.schemas import RoleModel
from src.repository import roles as repository_roles
from src.services.auth_admin import is_admin


router = APIRouter(prefix='/roles', tags=["roles"])
security = HTTPBearer()


@router.post("/create", status_code=status.HTTP_201_CREATED,
             response_model=RoleModel, dependencies=[Depends(is_admin)]
             )
async def post_role(
        id: int = Form(...),
        role_name: str = Form(...),
        db: AsyncSession = Depends(get_db),
):
    """
    Create a new user role.

    :param id: The unique identifier for the new user role.
    :type id: int
    :param role_name: The name of the new user role.
    :type role_name: str
    :param current_user: The currently authenticated user.
    :type current_user: User
    :param db: The database session.
    :type db: AsyncSession
    :return: The newly created user role.
    :rtype: RoleModel
    """

    role = await repository_roles.create_role(id, role_name, db)

    if role:
        return role
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.put("/update", response_model=RoleModel, dependencies=[Depends(is_admin)])
async def update_role(
        id: int = Form(...),
        role_name: str = Form(...),
        db: AsyncSession = Depends(get_db),
):
    """
    Update the name of a user role.

    :param id: The unique identifier of the user role to update.
    :type id: int
    :param role_name: The new name for the user role.
    :type role_name: str
    :param current_user: The currently authenticated user.
    :type current_user: User
    :param db: The database session.
    :type db: AsyncSession
    :return: The updated user role.
    :rtype: RoleModel
    """

    role = await repository_roles.update_role(id, role_name, db)

    if role:
        return role
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
