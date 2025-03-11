from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(
        TIMESTAMP, nullable=False, server_default=func.current_timestamp(), default=func.current_timestamp()
    )
    updated_at = Column(
        TIMESTAMP, nullable=False, server_default=func.current_timestamp(), default=func.current_timestamp()
    )
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    topics = relationship("Topic", back_populates="user")
    comments = relationship("Comment", back_populates="user")
