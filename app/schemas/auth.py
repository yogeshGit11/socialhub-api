from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str]

class RefreshToken(BaseModel):
    refresh_token: str