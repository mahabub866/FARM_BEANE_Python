from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
import json


class RoleOut(BaseModel):
    role_id: UUID
    name: str
    
class Category(BaseModel):
    user_management: bool=True
    app_management: bool=True
    book_management: bool=True
    pop_management: bool=True

    class Config:
        orm_mode=True
    

class RoleSuperCreate(BaseModel):
    
    name: str = Field(..., title='Name', max_length=20, min_length=1)
    Role: Category
    active: bool
    