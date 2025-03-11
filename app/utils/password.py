from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """
    비밀번호 체크
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """
    비밀번호 해싱
    """
    return pwd_context.hash(password) 