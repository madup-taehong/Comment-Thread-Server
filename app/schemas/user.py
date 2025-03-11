from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="이메일")
    username: str = Field(..., description="이름")
    password: str = Field(..., description="비밀번호")


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime

    class Config:
        orm_mode = True
