from typing import List
import logging

from fastapi import UploadFile, HTTPException, status, APIRouter, File
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.templates.get_txt_from_pdf import get_txt_from_pdf

router = APIRouter(prefix='/pdffile', tags=['PDFfile'])


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_pdf(file: UploadFile = File()):
    try:
        await get_txt_from_pdf(file)
        return {"success": True}
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found or some other error message")
