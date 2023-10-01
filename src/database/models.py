from datetime import datetime
import enum

import uuid
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Enum, Integer, func, Float, Table
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.schema import Table


Base = declarative_base()


class Role(enum.Enum):
    user = 'user'
    admin = 'admin'


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    user_role_enum = Column('roles', Enum(Role), default=Role.user)
    password = Column(String(255), nullable=False)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    phone = Column(String(255))
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
    banned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __str__(self):
        return f"{self.username}"


class Admin(Base):
    __tablename__ = 'admin'
    admin_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    is_active = Column(Boolean, default=False)
    last_visit = Column(DateTime, default=func.now())


class Chat(Base):
    __tablename__ = "chats"
    chat_id = Column(Integer, primary_key=True, index=True)
    title_chat = Column(String, nullable=False)
    file_url = Column(String, nullable=True)
    chat_data = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    user = relationship('User', backref="chats")


class ChatHistory(Base):
    __tablename__ = "chathistories"
    chat_history_id = Column(Integer, primary_key=True, index=True)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    chat_id = Column(Integer, ForeignKey("chats.chat_id"), nullable=True)
    user = relationship('User', backref="chathistories")
    chat = relationship('Chat', backref="chathistories")
