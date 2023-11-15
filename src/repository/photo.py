from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from src.database.models import Photo, Tag, User


async def add_photo(body: Photo, tags: List[str], current_user: User, db: AsyncSession, url: str) -> Photo:
    # Логіка для додавання фото в базу даних
    photo = Photo(**body.dict(), user_id=current_user.id, avatar=url)

    # Додаємо теги до фото
    for tag_name in tags:
        tag = await db.query(Tag).filter(Tag.tag_name == tag_name).first()
        tag = tag.scalar_one_or_none()
        if not tag:
            tag = Tag(tag_name=tag_name)
            db.add(tag)
            await db.commit()
            await db.refresh(tag)
        photo.tags.append(tag)

    db.add(photo)
    await db.commit()
    await db.refresh(photo)
    return photo


async def remove_photo(photo_id: int, current_user: User, db: AsyncSession) -> Photo:
    async with db.begin():
        photo = await db.execute(select(Photo).filter(Photo.id == photo_id, Photo.user_id == current_user.id))
        photo = photo.scalar_one_or_none()

        if not photo:
            return None

        await db.delete(photo)

    return photo


async def update_description(photo_id: int, body: Photo, current_user: User, db: AsyncSession) -> Photo:
    # Логіка для оновлення опису фото за ідентифікатором
    photo = await db.execute(select(Photo).filter(Photo.id == photo_id, Photo.user_id == current_user.id))
    photo = photo.scalar_one_or_none()

    if not photo:
        return None

    for key, value in body.dict().items():
        setattr(photo, key, value)

    await db.commit()
    await db.refresh(photo)
    return photo


async def see_photo(photo_id: int, current_user: User, db: AsyncSession) -> Photo:
    # Логіка для отримання фото за ідентифікатором
    photo = await db.execute(select(Photo).filter(Photo.id == photo_id))
    return photo.scalar_one_or_none()