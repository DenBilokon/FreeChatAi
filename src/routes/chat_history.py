from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.messages import ChatMessages
from src.database.db import get_db
from src.database.models import User, Role
from src.repository import chat_history as repository_history
from src.schemas.chat_history_schemas import ChatHistoryBase, ChatHistoryModel
from src.services.auth import auth_service
from src.services.roles import RolesAccess

router = APIRouter(prefix='/history', tags=["history"])

allowed_get_history = RolesAccess([Role.admin, Role.user])  # noqa
allowed_add_messages = RolesAccess([Role.user, Role.admin])  # noqa


@router.post("/{chat_id}", response_model=ChatHistoryModel, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(allowed_add_messages)])
async def create_message(chat_id: int, body: ChatHistoryBase, db: AsyncSession = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    new_message = await repository_history.create_message(chat_id, body, db, current_user)
    return new_message


@router.get("/{chat_id}", response_model=List[ChatHistoryModel], dependencies=[Depends(allowed_get_history)])
async def get_history(chat_id: int, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    history = await repository_history.get_history_by_chat(chat_id, db)
    if history is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ChatMessages.CHAT_NOT_FOUND)
    return history
