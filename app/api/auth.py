from datetime import timedelta
from email.policy import default

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.utils.jwt import create_access_token
from app.utils.password import verify_password, get_password_hash
from app.config import settings
from app.models.user import User
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse
from app.db.database import db

auth_router = APIRouter(prefix=f"{settings.API_VERSION}/auth", tags=["Authentication"])


@auth_router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate):
    """
    회원가입 api
    """
    with db.session() as session:
        # 이메일 중복 확인
        db_user = session.query(User).filter(User.email == user_data.email).first()
        # 등록된 이메일인 경우 에러 처리
        if db_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 등록된 이메일입니다")

        # 사용자 추가
        hashed_password = get_password_hash(user_data.password)
        new_user = User(email=user_data.email, username=user_data.username, hashed_password=hashed_password)

        session.add(new_user)
        session.commit()
        session.refresh(new_user)

    return UserResponse(
        id=new_user.id, email=new_user.email, username=new_user.username, created_at=new_user.created_at
    )


@auth_router.post("/login", response_model=Token)
def login(login_data: OAuth2PasswordRequestForm = Depends()):
    """
    로그인 api
    """
    with db.session() as session:
        # 사용자 확인
        user = session.query(User).filter(User.email == login_data.username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="존재하지 않는 아이디 입니다.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="비밀번호가 유효하지 않습니다.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # 액세스 토큰 생성
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"email": user.email}, expires_delta=access_token_expires)

    return Token(access_token=access_token, token_type="bearer")
