from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends
from models.user_model import User
from .depends import get_current_user
from schemas.todo_schema import TodoOut, TodoCreate, TodoUpdate
from services.todo_service import TodoService
from models.todo_model import Todo
from fastapi.encoders import jsonable_encoder

todo_router = APIRouter()


@todo_router.get('/', summary="Get all todos of the user", response_model=List[TodoOut])
async def list(current_user: User = Depends(get_current_user)):
    return await TodoService.list_todos(current_user)

@todo_router.get("/all",summary="Get all todos ",)
async def get_documents(current_user: User = Depends(get_current_user)):
    collection = await Todo.find(fetch_links=True).to_list()
    return collection

@todo_router.get("/all/without",summary="Get all todos without links ",response_model=List[TodoOut])
async def get_documents(current_user: User = Depends(get_current_user)):
    collection = Todo

    documents = []
    async for document in collection.find():

        documents.append(document)
       
    return documents


@todo_router.post('/create', summary="Create Todo", response_model=Todo)
async def create_todo(data: TodoCreate, current_user: User = Depends(get_current_user)):
    return await TodoService.create_todo(current_user, data)


@todo_router.get('/{todo_id}', summary="Get a todo by todo_id", response_model=TodoOut)
async def retrieve(todo_id: UUID, current_user: User = Depends(get_current_user)):
    return await TodoService.retrieve_todo(current_user, todo_id)


@todo_router.put('/{todo_id}', summary="Update todo by todo_id", response_model=TodoOut)
async def update(todo_id: UUID, data: TodoUpdate, current_user: User = Depends(get_current_user)):
    return await TodoService.update_todo(current_user, todo_id, data)


@todo_router.delete('/{todo_id}', summary="Delete todo by todo_id")
async def delete(todo_id: UUID, current_user: User = Depends(get_current_user)):
    await TodoService.delete_todo(current_user, todo_id)
    return None