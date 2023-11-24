from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession

import src.repository.comments as repository_comments
from src.database.db import get_db
from src.database.models import User
from src.services.auth import auth_service
from src.schemas import CommentSchema, CommentUpdateSchems, CommentRemoveSchema

THE_MANY_REQUESTS = "No more than 10 requests in a minute"
DELETED_SUCCESSFUL = "Comment deleted successfully"

router = APIRouter(prefix="/comments", tags=['Comments'])


@router.post("/publish", status_code=status.HTTP_201_CREATED,
             description=THE_MANY_REQUESTS,
             response_model=CommentSchema)
async def post_comment(
        photo_id: int = Form(...),
        text: str = Form(...),
        current_user: User = Depends(auth_service.get_current_user),
        db: AsyncSession = Depends(get_db),
):
    """
    Publish a comment on a photo.

    :param photo_id: ID of the photo to comment on.
    :type photo_id: int
    :param text: The text of the comment.
    :type text: str
    :param current_user: The authenticated user.
    :type current_user: User
    :param db: Database session.
    :type db: AsyncSession

    :return: Comment object if successful.
    :rtype: dict

    :raises HTTPException: If the comment could not be created.
    :rtype: HTTPException
    """
    comment = await repository_comments.create_comments(text, current_user, photo_id, db)

    if comment:
        return comment
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.patch(
    "/update",
    status_code=status.HTTP_200_OK, response_model=CommentUpdateSchems)
async def change_comment(
        comment_id: int = Form(...),
        text: str = Form(...),
        current_user: User = Depends(auth_service.get_current_user),
        db: AsyncSession = Depends(get_db),
):
    """
    Update a comment.

    :param comment_id: ID of the comment to be updated.
    :type comment_id: int
    :param text: The new text for the comment.
    :type text: str
    :param current_user: The authenticated user.
    :type current_user: User
    :param db: Database session.
    :type db: AsyncSession

    :return: Updated comment if successful.
    :rtype: dict

    :raises HTTPException 404: If the comment does not exist.
    :raises HTTPException 403: If the current user is not the author of the comment.
    """
    comment_check = await repository_comments.get_comment(comment_id, db)
    if comment_check:
        if comment_check.user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
        comment = await repository_comments.update_comment(text, comment_id, db)
        return comment
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/delete", status_code=status.HTTP_200_OK)
async def remove_comment(
        comment_id: int = Form(...),
        current_user: User = Depends(auth_service.get_current_user),
        db: AsyncSession = Depends(get_db),
):
    """
    Delete a comment.

    :param comment_id: ID of the comment to be deleted.
    :type comment_id: int
    :param current_user: The authenticated user.
    :type current_user: User
    :param db: Database session.
    :type db: AsyncSession

    :return: A response indicating the success of the deletion.
    :rtype: dict

    :raises HTTPException 404: If the comment does not exist.
    :raises HTTPException 403: If the current user is not the author of the comment and is not a moderator or admin.
    """
    comment = await repository_comments.get_comment(comment_id, db)
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if current_user.role_id not in [1, 2]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You don't have permission to delete this comment.")

    await repository_comments.delete_comment(comment_id, db)
    return {"detail": DELETED_SUCCESSFUL}


@router.get("/photos/{photo_id}", response_model=List[CommentSchema])
async def show_photo_comments(
        photo_id: int,
        limit: int = 0,
        offset: int = 10,
        current_user: User = Depends(auth_service.get_current_user),
        db: AsyncSession = Depends(get_db),
):
    """
    Retrieve comments for a specific photo.

    :param photo_id: The ID of the photo for which comments are to be retrieved.
    :type photo_id: int
    :param limit: The maximum number of comments to retrieve (default is 0, which retrieves all).
    :type limit: int
    :param offset: The offset for paginating through comments (default is 10).
    :type offset: int
    :param current_user: The authenticated user.
    :type current_user: User
    :param db: Database session.
    :type db: AsyncSession

    :return: A dictionary containing the list of comments for the specified photo.
    :rtype: dict

    :raises HTTPException 404: If the photo does not exist.
    """
    comments = await repository_comments.get_photo_comments(limit, offset, photo_id, current_user, db)
    if comments:
        return comments
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.get("/users/{users_id}", response_model=List[CommentSchema])
async def show_user_comments(
        user_id: int,
        limit: int = 0,
        offset: int = 10,
        current_user: User = Depends(auth_service.get_current_user),
        db: AsyncSession = Depends(get_db),
):
    """
    Retrieve comments for a specific user.

    :param user_id: The ID of the user for whom comments are to be retrieved.
    :type user_id: int
    :param limit: The maximum number of comments to retrieve (default is 0, which retrieves all).
    :type limit: int
    :param offset: The offset for paginating through comments (default is 10).
    :type offset: int
    :param current_user: The authenticated user.
    :type current_user: User
    :param db: Database session.
    :type db: AsyncSession

    :return: A dictionary containing the list of comments for the specified user.
    :rtype: dict

    :raises HTTPException 404: If the user does not exist.
    """
    comments = await repository_comments.get_user_comments(limit, offset, user_id, db)
    if comments:
        return comments
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
