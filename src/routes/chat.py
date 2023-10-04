import logging

from fastapi import HTTPException, APIRouter, Request, Form
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.database.models import User, Chat, ChatHistory
from src.schemas.user_schemas import UserModel
from src.services.vector_doc_ai import vector_func

router = APIRouter(prefix='/chat', tags=['chat'])


@router.post("/ask", status_code=status.HTTP_201_CREATED)
async def post_question(request: Request, question: str = Form(...)):
    path_to_file = request.session.get("current_path_document")
    print(path_to_file)

    if not path_to_file:
        raise HTTPException(status_code=400, detail="Error path_to_file.")
    response = await vector_func(path_to_file, question)
    # print(response)
    return {"response": response}
