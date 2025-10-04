from pydantic import BaseModel
from datetime import datetime

class CommentCreate(BaseModel):
    content: str

class CommentOut(BaseModel):
    id: int
    content: str
    author_id: int
    post_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class PostComments(BaseModel):
    content: str
    author_id: int
    created_at: datetime
