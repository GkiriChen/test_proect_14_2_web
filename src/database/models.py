import enum

from datetime import datetime, date

from sqlalchemy import Column, Integer, Text, String, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()


## ----Create ----#

class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String, unique=True, index=True)

    users = relationship("User", back_populates="role")

    __allow_unmapped__ = True

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    role_id = Column('role_id', ForeignKey(
        'userroles.id', ondelete='CASCADE'), default=3)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    ban = Column(Boolean, default=False)


class Photo(Base):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="photos")
    comments: Mapped[list["Comment"]] = relationship(
        "Comment", back_populates="photo", cascade="all, delete-orphan"
    )


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[date] = mapped_column("created_at", DateTime, default=func.now())
    updated_at: Mapped[date] = mapped_column("updated_at", DateTime, default=func.now(), onupdate=func.now())
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    photo_id: Mapped[int] = mapped_column("photos_id", ForeignKey("photos_id", ondelete="CASCADE"), default=None)
    update_status: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped[int] = relationship("User", backref="comments")
    photo: Mapped["Photo"] = relationship("Photo", back_populates="comments")
