from typing import List
from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import Photo, Tag, User
from src.services.auth import auth_service
from src.repository.photo import add_photo

from src.schemas import PhotoModels, ImageTagResponse, PhotoBase

router = APIRouter(prefix='/photos', tags=["photos"])

@router.post("/", response_model=PhotoModels)
async def add_photo(
    body: PhotoBase,
    tags: List[ImageTagResponse] = [],
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
    file: UploadFile = File(...),
):
    # Зберігаємо фото в базу даних
    return await add_photo(body, tags, current_user, db, file)

@router.delete("/{photo_id}", response_model=PhotoModels)
async def remove_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return await remove_photo(photo_id, current_user, db)

@router.put("/{photo_id}", response_model=PhotoModels)
async def update_description(
    body: PhotoBase,
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return await update_description(photo_id, body, current_user, db)

@router.get("/{photo_id}", response_model=PhotoModels)
async def see_photo(
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    return await see_photo(photo_id, current_user, db)
