from fastapi import FastAPI
from src.posts import router as posts_router, models
from src.config import settings
from health.router import router as health_router
from src.users.router import router as users_router
# from src.database import engine,Base
# import asyncio

# app = FastAPI(title=settings.APP_NAME)
# # 创建事件-->启动时创建数据表
# async def create_db_tables():
#     async with engine.begin() as conn:  # 异步处理上下文
#         await conn.run_sync(Base.metadata.create_all)
#
# @app.on_event("startup")
# async def on_startup():
#     print("startup...")
#     await create_db_tables()
#     print("over")

app = FastAPI(title=settings.APP_NAME)

app.include_router(health_router)
app.include_router(posts_router.router)
app.include_router(users_router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to my practice","环境":settings.ENVIRONMENT}
