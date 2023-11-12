import src.repository.comments as repository_comments
from src.database.db import get_db
from fastapi import APIRouter, Depends, status, HTTPException, Form
from fastapi_limiter.depends import Ratelimiter
from src.services.auth import Auth
from src.database.models import User, UserRole
from sqlalchemy.ext.asyncio import AsyncSession

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
        current_user: User = Depends(Auth.get_current_user),
        db: AsyncSession = Depends(get_db),
):
    comment = await repository_comments.create_comments(text, current_user, photo_id, db)

    if comment:
        return comment
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.patch(
    "/update",
    status_code=status.HTTP_200_OK,
)
async def change_comment(
        comment_id: int = Form(...),
        text: str = Form(...),
        current_user: User = Depends(Auth.get_current_user),
        db: AsyncSession = Depends(get_db),
):
    comment_check = await repository_comments.get_comment(comment_id, db)
    if comment_check:
        if comment_check.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        comment = await repository_comments.update_comment(text, comment_id, db)
        return comment
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/delete")
async def remove_comment(
        comment_id: int = Form(...),
        current_user: User = Depends(Auth.get_current_user),
        db: AsyncSession = Depends(get_db),
):
    comment = await repository_comments.get_comment(comment_id, db)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if comment.user_id != current_user.id and current_user.role not in [
        UserRole.Moderator,
        UserRole.Admin,
    ]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    await repository_comments.delete_comment(comment_id, db)
    return {"detail": DELETED_SUCCESSFUL}


@router.get("/photos/{photo_id}")
async def show_photo_comments(
        photo_id: int,
        limit: int = 0,
        offset: int = 10,
        current_user: User = Depends(Auth.get_current_user),
        db: AsyncSession = Depends(get_db),
):
    comments = await repository_comments.get_photo_comments(limit, offset, photo_id, db)
    return {"comments": comments}


@router.get("/users/{users_id}")
async def show_user_comments(
        user_id: int,
        limit: int = 0,
        offset: int = 10,
        current_user: User = Depends(Auth.get_current_user),
        db: AsyncSession = Depends(get_db),
):
    comments = await repository_comments.get_user_comments(limit, offset, user_id, db)
    return {"comments": comments}
