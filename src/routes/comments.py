from src.database.db import get_db
from fastapi import APIRouter, Depends, status, HTTPException, Form
from fastapi_limiter.depends import Ratelimiter

THE_MANY_REQUESTS = "No more than 10 requests in minute"
DELETED_SUCCESSFUL = "You deleted SUCCESSFUL"

router = APIRouter(prefix="/comments", tags=['Comments'])


@router.post("/publish", status_code=status.HTTP_201_CREATED,
             description=THE_MANY_REQUESTS,
             dependencies=[Depends(Ratelimiter(times=10, seconds=60))],
             )
async def post_comment(
        photo_id: int = Form(...),
        text: str = Form(...),
        current_user: User = Depends()

)