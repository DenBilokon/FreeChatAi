from datetime import datetime
import enum

import uuid
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Enum, Integer, func, Float, Table
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.schema import Table


Base = declarative_base()


class Role(enum.Enum):
    client = 'client'
    admin = 'admin'


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    user_role = Column('role', Enum(Role), default=Role.client)
    password = Column(String(255), nullable=False)
    name = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    country_id = Column(Integer, ForeignKey("countries.country_id"), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.city_id"), nullable=False)
    phone = Column(String(255))
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    banned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __str__(self):
        return f"{self.name}"


class Admin(Base):
    __tablename__ = 'admin'
    admin_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    is_active = Column(Boolean, default=False)
    last_visit = Column(DateTime, default=func.now())
