from fastapi import APIRouter, HTTPException,Depends,status
from models.role_model import Role
from models.user_model import User
from schemas.role_schema import RoleOut
from typing import List
from beanie import PydanticObjectId
from bson import ObjectId
from uuid import UUID
from .depends import get_current_user
role_router = APIRouter()


@role_router.post("/mymodel")
async def create_mymodel(item: Role,current_user: User = Depends(get_current_user)):

    
    await item.create()
    return item

@role_router.get("/all", status_code=200)
async def getalltasks(current_user: User = Depends(get_current_user))  :
  
    product = await User.find_one(User.email == str(current_user))
    print(product.user_id)
    print(product.status)
    # tasks = await Role.find_all().to_list()
    # return tasks
    if product.status==True:
        tasks = await Role.find_all().to_list()
        return tasks
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User is inactive")
       

@role_router.put("/{role_id}", status_code=200)
async def updateTask(role: Role, role_id: UUID) -> Role:
    task_to_update = await Role.find_one(Role.role_id==role_id)
    

    if not task_to_update:
        raise HTTPException(status_code=404, detail="Resource not found")
    task_to_update.name = role.name
    task_to_update.active = role.active
    task_to_update.Role.app_management = role.Role.app_management
    task_to_update.Role.user_management = role.Role.user_management
    task_to_update.Role.book_management = role.Role.book_management
    task_to_update.Role.pop_management = role.Role.pop_management
    
    await task_to_update.save()

    return task_to_update

@role_router.get("/{role_id}", status_code=200)
async def retrieveTask(role_id: UUID) -> Role:

    task_to_get = await Role.find_one(Role.role_id==role_id)

    return task_to_get

@role_router.delete("/{role_id}", status_code=204)
async def deleteTask(role_id: UUID):
    task_to_delete = await Role.find_one(Role.role_id==role_id)

    await task_to_delete.delete()

    return {"message": "Task deleted"}