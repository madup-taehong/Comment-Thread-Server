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

    input:
        user_id: 조회할 사용자의 ID

    output:
        UserResponse: 조회된 사용자 정보

    error:
        사용자가 존재하지 않는 경우 404 에러 발생
    """
    with db.session() as session:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다")
        return user
