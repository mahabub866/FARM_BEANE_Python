from fastapi import FastAPI, HTTPException, Depends, status
from core.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from models.user_model import User
from api.api_1.router import router
from models.todo_model import Todo
from models.task_model import Task
from models.demo_model import Demo
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.on_event("startup")
async def app_init():
    """
        initialize crucial application services
    """
    
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).fodoist                         #create the database name fodolist
    
    await init_beanie(
        database=db_client,
        document_models= [                               #all the models name give here
           User,
           Todo,
           Task,
           Demo
        ]
    )


app.include_router(router,prefix=settings.API_V1_STR)