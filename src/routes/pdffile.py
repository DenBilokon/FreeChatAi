from io import BytesIO
from typing import List
import logging

from PyPDF2 import PdfReader
from fastapi import UploadFile, HTTPException, status, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix='/pdffile', tags=['pdffile'])


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def get_txt_from_pdf(file: UploadFile) -> dict:

    try:

        file_name, extension = file.filename.split('.')
        if extension != 'pdf':
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only PDF file can be downloaded.")

        file_content = await file.read()
        pdf_file = BytesIO(file_content)
        pdf_reader = PdfReader(pdf_file)
        text = ''

        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text()

        with open(f"{file_name}.txt", 'w', encoding="utf-8") as txt:
            txt.write(text)

        return {'filename': file_name, 'text': text}

    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Upload PDFfile")
