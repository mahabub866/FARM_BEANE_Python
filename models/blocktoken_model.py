from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4
from beanie import Document, Indexed
from pydantic import Field, EmailStr

class Block(Document):
    block_id: UUID = Field(default_factory=uuid4)
    token: Indexed(str, unique=True)
    user_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Collection:
        name = "blocks"