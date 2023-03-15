from typing import Optional,Dict

import pymongo
from pydantic import BaseModel

from beanie import Document, Indexed


class Category(BaseModel):
    name: str
    description: str


class Demo(Document):  # This is the model
    name: str
    description: Optional[str] = None
    price: Indexed(float, pymongo.DESCENDING)
    category: Category
    role: Dict[str, bool]

    class Settings:
        use_state_management = True
        state_management_replace_objects = True