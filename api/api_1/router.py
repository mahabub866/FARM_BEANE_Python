from fastapi import APIRouter
from api.api_1 import user,auth,todo
router = APIRouter()

router.include_router(user.user_router,prefix='/users',tags=["users"])
router.include_router(auth.auth_router,prefix='/auth',tags=["authentication"])
router.include_router(todo.todo_router, prefix='/todo', tags=["todo"])