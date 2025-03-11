from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.schemas.comment import CommentResponse
from app.schemas.user import UserResponse


class TopicBase(BaseModel):
    title: str = Field(..., min_length=1, description="제목")
    content: str = Field(..., min_length=1, description="내용")


class TopicCreate(TopicBase):
    pass


class TopicResponse(TopicBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    user_id: int
    user: Optional[UserResponse] = None
    comments: List[CommentResponse] = None

    class Config:
        orm_mode = True
