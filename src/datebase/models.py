import enum

from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime

Base = declarative_base()

## ----Create ----#


class UserRole(int, enum.Enum):
    Admin = 1
    Moderator = 2
    User = 3


class User(Base):
    __tablename__ = "users"
