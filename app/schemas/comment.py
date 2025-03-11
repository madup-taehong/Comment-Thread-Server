from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from app.schemas.user import UserResponse


class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, description="댓글 내용")


class CommentCreate(CommentBase):
    topic_id: int
    parent_id: Optional[int] = None


class CommentResponse(CommentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    topic_id: int
    user_id: int
    parent_id: Optional[int] = None
    depth: int = 0
    user: Optional[UserResponse] = None
    replies: List[CommentResponse] = None

    class Config:
        orm_mode = True
