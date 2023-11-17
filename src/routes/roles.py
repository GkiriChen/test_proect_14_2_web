from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Form
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from src.database.db import get_db
from src.schemas import RoleModel
from src.repository import roles as repository_roles



router = APIRouter(prefix='/roles', tags=["roles"])
security = HTTPBearer()


@router.post("/create", status_code=status.HTTP_201_CREATED,
             response_model=RoleModel
             )
async def post_role(
        id: int = Form(...),
        role_name: str = Form(...),
        db: AsyncSession = Depends(get_db),
):
    role = await repository_roles.create_role(id, role_name, db)

    if role:
        return role
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
