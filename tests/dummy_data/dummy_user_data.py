from app.models import User
from app.utils.password import get_password_hash

dummy_user_data = [
    User(id=1, username="test_user1", email="test@test.com", hashed_password=get_password_hash("test")),
    User(id=2, username="test_user2", email="test2@test.com", hashed_password=get_password_hash("test")),
]
