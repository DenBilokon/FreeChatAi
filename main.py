# import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI

# from fastapi_limiter import FastAPILimiter
from src.conf.config import settings
from sqladmin import Admin

from src.database.db import create_async_engine

from src.routes import auth, users


engine = create_async_engine(settings.sqlalchemy_database_url)


# Створюємо екземпляр FastApi, встановлюємо назву додатка у swagger та відсортуємо роути по методах:
from src.services.admin_panel.admin_panel import UserAdmin

app = FastAPI(swagger_ui_parameters={"operationsSorter": "method"}, title='FreeChatAI app')

# підключаємо адмін-панель
# http://localhost:8001/admin/
admin = Admin(app, engine)
admin.add_view(UserAdmin)



@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!"}


# @app.on_event("startup")
# async def startup():
#     r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, password=settings.redis_password,
#     encoding="utf-8", db=0)
#     await FastAPILimiter.init(r)

app.include_router(auth.router, prefix='/api')
# app.include_router(users.router, prefix='/api')


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)