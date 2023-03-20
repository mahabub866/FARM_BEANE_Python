from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field

class BlockCreate(BaseModel):
    user_id: str = Field(..., title='user id', max_length=55, min_length=1)
    token: str = Field(..., title='token', max_length=755, min_length=1)
    
    
    