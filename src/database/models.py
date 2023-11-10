import enum

from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()

## ----Create ----#


class UserRole(Base):
    __tablename__ = "userroles"
    id = Column(Integer, primary_key=True)
    role_name = Column(String(50))


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


