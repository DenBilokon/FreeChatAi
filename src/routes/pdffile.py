from pathlib import Path
from typing import List
import logging

from fastapi import UploadFile, HTTPException, status, APIRouter, File, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix='/pdffile', tags=['PDFfile'])


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_pdf(request: Request, file: UploadFile = File(...)):
    try:
        file_name, extension = file.filename.split('.')
        if extension != 'pdf':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="підтримує тільки PDF")

        save_path = Path("uploaded_files") / file.filename

        save_path.parent.mkdir(parents=True, exist_ok=True)

        with save_path.open("wb") as buffer:
            buffer.write(await file.read())

        # Зберігаємо шлях до файлу у сесії
        request.session["current_path_document"] = str(save_path.absolute())
        return {"success": True, 'filename': file_name, 'path': str(save_path.absolute())}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Помилка при завантаженні файлу: {e}")
