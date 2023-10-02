import logging

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.models import User, Chat, ChatHistory
from src.schemas.user_schemas import UserModel

