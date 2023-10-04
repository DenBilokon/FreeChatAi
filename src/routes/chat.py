from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Query, Request, Form
from sqlalchemy.ext.asyncio import AsyncSession

from src.conf.messages import ChatMessages
from src.database.db import get_db
from src.database.models import User, Role
from src.repository import chats as repository_chats
from src.schemas.chat_schemas import ChatBase, ChatModel
from src.services.auth import auth_service
from src.services.roles import RolesAccess
from src.services.vector_doc_ai import vector_func

router = APIRouter(prefix='/chats', tags=["chats"])

allowed_get_chats = RolesAccess([Role.admin, Role.user])  # noqa
allowed_add_chats = RolesAccess([Role.admin, Role.user])  # noqa
allowed_delete_chats = RolesAccess([Role.admin, Role.user])  # noqa


@router.post("/ask", status_code=status.HTTP_201_CREATED)
async def post_question(request: Request, question: str = Form(...)):
    path_to_file = request.session.get("current_path_document")
    print(path_to_file)

    if not path_to_file:
        raise HTTPException(status_code=400, detail="Error path_to_file.")
    response = await vector_func(path_to_file, question)
    # print(response)
    return {"response": response}


@router.post("/", response_model=ChatModel, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(allowed_add_chats)])
async def create_chat(body: ChatBase, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    new_chat = await repository_chats.create_chat(body, db, current_user)
    return new_chat


@router.get("/", response_model=List[ChatModel], status_code=status.HTTP_200_OK,
            dependencies=[Depends(allowed_get_chats)])
async def get_chats(limit: int = Query(10, le=50), offset: int = 0,
                    current_user: User = Depends(auth_service.get_current_user),
                    db: AsyncSession = Depends(get_db)):
    chats = await repository_chats.get_chats(limit, offset, current_user, db)
    if chats is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ChatMessages.NOT_FOUND)
    return chats


@router.get("/{chat_id}", response_model=ChatModel, dependencies=[Depends(allowed_get_chats)])
async def get_chat(chat_id: int, db: AsyncSession = Depends(get_db),
                   current_user: User = Depends(auth_service.get_current_user)):
    chat = await repository_chats.get_chat_by_id(chat_id, db, current_user)
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ChatMessages.CHAT_NOT_FOUND)
    return chat


@router.delete("/{chat_id}", response_model=ChatModel,
               dependencies=[Depends(allowed_delete_chats)])
async def delete_chat(chat_id: int, db: AsyncSession = Depends(get_db),
                      current_user: User = Depends(auth_service.get_current_user)):
    deleted_chat = await repository_chats.delete_chat(chat_id, db, current_user)
    if deleted_chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ChatMessages.CHAT_NOT_FOUND)
    return deleted_chat

