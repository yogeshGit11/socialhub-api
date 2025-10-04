from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .comment import PostComments


class PostCreate(BaseModel):
    content: str
    image: Optional[str]


class PostOut(BaseModel):
    id: int
    content: str
    image: Optional[str]
    author_id: int
    created_at: datetime
    comments: List[PostComments] = []

    model_config = {"from_attributes": True}
