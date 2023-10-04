# import redis.asyncio as redis
import uvicorn
from dotenv import load_dotenv

from fastapi import FastAPI, Request, Form, HTTPException, UploadFile, File, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

# from fastapi_limiter import FastAPILimiter
from src.conf.config import settings
from sqladmin import Admin

from src.database.db import create_async_engine
from src.services.admin_panel.admin_panel import UserAdmin
from src.routes import auth, users, pdffile, chat, chat_history


engine = create_async_engine(settings.sqlalchemy_database_url)

load_dotenv()

# Створюємо екземпляр FastApi, встановлюємо назву додатка у swagger та відсортуємо роути по методах:
app = FastAPI(swagger_ui_parameters={"operationsSorter": "method"}, title='FreeChatAI app')
app.add_middleware(SessionMiddleware, secret_key="some-random-secret-key")

# підключаємо адмін-панель
# http://localhost:8001/admin/
admin = Admin(app, engine)
admin.add_view(UserAdmin)

templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')
app.include_router(pdffile.router)
app.include_router(chat.router)
app.include_router(chat_history.router)


@app.get("/", response_class=HTMLResponse, tags=["Main index.html"])
async def root(request: Request):
    return templates.TemplateResponse('index.html', {'request': request, "response": None})


# @app.on_event("startup")
# async def startup():
#     r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, password=settings.redis_password,
#     encoding="utf-8", db=0)
#     await FastAPILimiter.init(r)

if __name__ == '__main__':
    uvicorn.run('main:app', port=8080, reload=True)
