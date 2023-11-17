from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import UserRole


async def create_role(id: int, name: str, db: AsyncSession) -> UserRole:
    
    role = UserRole(id=id, role_name=name)
    
    try:
        db.add(role)
        await db.commit()
        await db.refresh(role)
        return role
    except Exception as e:
        await db.rollback()
        raise e
