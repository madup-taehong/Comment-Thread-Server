# reference : https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.db.database import db
from app.models.user import User
from app.schemas.token import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_VERSION}/auth/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    액세스 토큰 생성 함수

    input:
        data: 토큰에 인코딩할 데이터
        expires_delta: 토큰 만료 시간. 기본값은 None.

    output:
        str: 생성된 JWT 토큰

    참고자료:
        - python-jose 문서: https://python-jose.readthedocs.io/en/latest/jwt/api.html
        - JWT 표준 규격: https://datatracker.ietf.org/doc/html/rfc7519
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    """
    토큰 검증 함수

    input:
        token: 검증할 JWT 토큰
        credentials_exception: 인증 실패 시 발생시킬 예외

    output:
        TokenData: 토큰에서 추출한 데이터

    error:
        credentials_exception: 토큰이 유효하지 않을 경우 발생

    참고자료:
        - python-jose 문서: https://python-jose.readthedocs.io/en/latest/jwt/api.html#jose.jwt.decode
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
        return token_data
    except JWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    현재 사용자 가져오기

    input:
        token: OAuth2 스키마로부터 얻은 JWT 토큰. Depends(oauth2_scheme)로 자동 주입됨.

    output:
        User: 현재 인증된 사용자 객체

    error:
        HTTPException: 인증 정보가 유효하지 않을 경우 발생

    참고자료:
        - FastAPI OAuth2 문서: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
    """
    with db.session() as session:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증 정보가 유효하지 않습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )

        # 토큰 검증
        token_data = verify_token(token, credentials_exception)

        # 사용자 조회
        user = session.query(User).filter(User.email == token_data.email).first()
        if user is None:
            raise credentials_exception

        return user
