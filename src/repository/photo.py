from typing import List
from sqlalchemy.orm import Session
from src.database.models import Photo, Tag, User

async def add_photo(body: Photo, tags: List[str], current_user: User, db: Session, url: str) -> Photo:
    # Логіка для додавання фото в базу даних
    photo = Photo(**body.dict(), user_id=current_user.id, avatar=url)
    
    # Додаємо теги до фото
    for tag_name in tags:
        tag = db.query(Tag).filter(Tag.tag_name == tag_name).first()
        if not tag:
            tag = Tag(tag_name=tag_name)
            db.add(tag)
            db.commit()
            db.refresh(tag)
        photo.tags.append(tag)

    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo

async def remove_photo(photo_id: int, current_user: User, db: Session) -> Photo:
    # Логіка для видалення фото з бази даних за ідентифікатором
    photo = db.query(Photo).filter(Photo.id == photo_id, Photo.user_id == current_user.id).first()
    if not photo:
        return None
    db.delete(photo)
    db.commit()
    return photo

async def update_description(photo_id: int, body: Photo, current_user: User, db: Session) -> Photo:
    # Логіка для оновлення опису фото за ідентифікатором
    photo = db.query(Photo).filter(Photo.id == photo_id, Photo.user_id == current_user.id).first()
    if not photo:
        return None
    for key, value in body.dict().items():
        setattr(photo, key, value)
    db.commit()
    db.refresh(photo)
    return photo

async def see_photo(photo_id: int, current_user: User, db: Session) -> Photo:
    # Логіка для отримання фото за ідентифікатором
    photo = db.query(Photo).filter(Photo.id == photo_id).first()
    return photo
