from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
import json


class RoleOut(BaseModel):
    role_id: UUID
    name: str
    
    

 