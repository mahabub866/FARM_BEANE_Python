from datetime import datetime
from beanie import Document, PydanticObjectId
from pydantic import Field
from bson.objectid import ObjectId
from uuid import UUID, uuid4
from pydantic import BaseModel
from typing import Optional


class Category(BaseModel):
    user_management: Optional[bool]=False
    app_management: Optional[bool]=False
    book_management: Optional[bool]=False
    pop_management: Optional[bool]=False

    class Config:
        orm_mode=True


class Role(Document):
    role_id: UUID = Field(default_factory=uuid4)
    name: str = Field(max_length=100,unique=True,description="role name")
    active: bool = False
    Role: Category
    create_at: datetime = datetime.now()

    class Settings:
        use_state_management = True
        state_management_replace_objects = True
    class Config:
        orm_mode=True
    class Collection:
        name = "role"

