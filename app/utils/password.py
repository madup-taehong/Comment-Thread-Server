# reference : https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """
    비밀번호 체크

    input:
        plain_password: 평문 비밀번호
        hashed_password: 해시된 비밀번호

    output:
        bool: 비밀번호가 일치하면 True, 그렇지 않으면 False
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    비밀번호 해싱

    input:
        password: 해싱할 평문 비밀번호

    output:
        str: 해시된 비밀번호
    """
    return pwd_context.hash(password)
