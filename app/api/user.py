from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import settings
from app.db.database import db
from app.models.user import User
from app.schemas.user import UserResponse

user_router = APIRouter(prefix=f"{settings.API_VERSION}/users", tags=["Users"])


@user_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """
    사용자 조회 api
    """
    with db.session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다")
        return user
