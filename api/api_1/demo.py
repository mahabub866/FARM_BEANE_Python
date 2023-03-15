from fastapi import APIRouter, HTTPException
from models.demo_model import Demo
from typing import List
from beanie import PydanticObjectId
from bson import ObjectId

demo_router = APIRouter()


@demo_router.post("/mymodel")
async def create_mymodel(item: Demo):
    await item.create()
    return {"id": str(item.id)}

@demo_router.get("/all", status_code=200)
async def getalltasks() -> List[Demo]:
    tasks = await Demo.find_all().to_list()

    return tasks
