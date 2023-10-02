from io import BytesIO
from typing import List
import logging

from PyPDF2 import PdfReader
from fastapi import UploadFile, HTTPException, status, APIRouter


async def get_txt_from_pdf(file) -> dict:
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

        # with open(f"{file_name}.txt", 'w', encoding="utf-8") as txt:
        #     txt.write(text)
        # print(file_name)

        return {'filename': file_name, 'text': text, 'file_txt': f"{file_name}.txt"}

    except Exception as ex:

        raise ex
