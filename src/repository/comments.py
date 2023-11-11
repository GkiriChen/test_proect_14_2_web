from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.models import Comment


async def create_comments(content: str, user: str, photos_id: int, db: AsyncSession):
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
    comment = await db.get(Comment, id)
    return comment


async def update_comment(text: str, id: int, db: AsyncSession):
    comment = await db.get(Comment, id)
    if comment:
        try:
            comment.text = text
            comment.update_status = True
            await db.commit()
            await db.refresh(comment)
            return comment
        except Exception as e:
            await db.rollback()
            raise e
    return None


async def delete_comment(id: int, db: AsyncSession):
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


async def get_photo_comments(offset: int, limit: int, photo_id: int, db: AsyncSession):
    sql = (select(Comment)
           # .options(selectinload(Comment.user))
           .filter(Comment.photo_id == photo_id)
           .offset(offset)
           .limit(limit))
    comments = await db.execute(sql)
    result = comments.scalars().all()
    return result


async def get_user_comments(offset: int, limit: int, user_id: int, db: AsyncSession):
    sql = (select(Comment)
           # .options(selectinload(Comment.user))
           .filter(Comment.user_id == user_id)
           .offset(offset)
           .limit(limit))
    comments = await db.execute(sql)
    result = comments.scalars().all()
    return result
