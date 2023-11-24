from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Comment


async def create_comments(content: str, user: str, photos_id: int, db: AsyncSession):
    """
    Creates a new comment and stores it in the database.

    :param content: str: Text of the comment.
    :param user: str: The user who left the comment.
    :param photos_id: int: The ID of the photo to which the comment is linked.
    :param db: AsyncSession: Database session to perform operations.
    :return: Comment: Comment created.
    :raises Exception: If an error occurred while creating the comment.
    """
    comment = Comment(text=content, user=user, photo_id=photos_id)
    try:
        db.add(comment)
        await db.commit()
        await db.refresh(comment)
        return comment
    except Exception as e:
        await db.rollback()
        raise e


async def get_comment(id: int, db: AsyncSession):
    """
    Get a Comment by ID

    This function retrieves a comment by its ID from the database.

    :param int id: The ID of the comment to retrieve.
    :param AsyncSession db: An asynchronous database session.
    :return: The comment with the specified ID, or None if the comment is not found.
    :rtype: Comment | None
    """
    comment = await db.get(Comment, id)
    if comment:
        return comment
    else:
        return None


async def update_comment(text: str, id: int, db: AsyncSession):
    """
    Update a comment

    :param text: The text for updating the comment
    :type content: str
    :param id: The ID of the comment to update
    :type id: int
    :param db: The database session.
    :type db: AsyncSession
    :return: The updated comment object.
    :rtype: Comment
    """
    comment = await db.get(Comment, id)
    if comment:
        try:
            comment.text = text
            comment.update_status = True
            comment.updated_at = datetime.now()
            await db.commit()
            await db.refresh(comment)
            return comment
        except Exception as e:
            await db.rollback()
            raise e
    return None


async def delete_comment(id: int, db: AsyncSession):
    """
    Delete a comment

    :param id: The ID of the comment to update
    :type comment_id: int
    :param db: The database session.
    :type db: AsyncSession
    :return: The comment object.
    :rtype: Comment
    """
    comment = await db.get(Comment, id)

    if comment:
        try:
            await db.delete(comment)
            await db.commit()
            return comment
        except Exception as e:
            await db.rollback()
            raise e
    return None


async def get_photo_comments(offset: int, limit: int, photo_id: int, user: int, db: AsyncSession):
    """
    Gets comments on a specific photo with pagination.

    :param offset: int: Offset to sample comments.
    :param limit: int: Maximum number of comments to sample.
    :param photo_id: int: Identifier of the photo to which the comments refer.
    :param db: AsyncSession: The database session for performing operations.
    :return: list[Comment]: Pagination-aware list of comments on the photo.
    """
    sql = await db.execute(select(Comment).filter(Comment.photo_id == photo_id, Comment.user_id == user.id).offset(offset).limit(limit))
    result = sql.fetchall()
    if result:
        comments = []
        for res in result:
            comments.append(res[0])
        return comments
    else:
        return None


async def get_user_comments(offset: int, limit: int, user_id: int, db: AsyncSession):
    """
    Review comments by photo

    :param limit: limit of comments
    :type: int
    :param offset: offset of comments
    :type offset: int
    :param photos_id: The ID of the photo for which to retrieve ratings.
    :type photos_id: int
    :param db: The database session.
    :type db: AsyncSession
    :return: A list of comment objects.
    :rtype: list[Comment]
    """
    sql = await db.execute(select(Comment)
                           .filter(Comment.user_id == user_id)
                           .offset(offset)
                           .limit(limit))
    result = sql.fetchall()
    if result:
        comments = []
        for res in result:
            comments.append(res[0])
        return comments
    else:
        return None
