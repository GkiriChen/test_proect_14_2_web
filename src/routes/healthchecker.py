from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database.db import get_db

router = APIRouter(prefix="/healthchecker", tags=["healthchecker"])


@router.get("/")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    """
    Endpoint for health checking the application and database connection.

    :param db: The asynchronous database session.
    :type db: AsyncSession

    :return: A dictionary with a welcome message if the application and database connection are healthy.
    :rtype: dict

    :raises HTTPException 500: If there is an error connecting to the database.
    """
    try:
        result = await db.execute(select(1))

        if result is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database is not configured correctly"
            )

        return {"message": "Welcome to FastAPI!"}
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database"
        )
