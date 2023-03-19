from fastapi import APIRouter
from api.api_1 import user,auth,todo,task,demo,role
router = APIRouter()

router.include_router(user.user_router,prefix='/users',tags=["users"])
router.include_router(auth.auth_router,prefix='/auth',tags=["authentication"])
router.include_router(todo.todo_router, prefix='/todo', tags=["todo"])
router.include_router(task.task_router, prefix="/tasks",tags=["task"])
router.include_router(demo.demo_router, prefix="/demo",tags=["demo"])
router.include_router(role.role_router, prefix="/role",tags=["role"])