from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(
        TIMESTAMP, nullable=False, server_default=func.current_timestamp(), default=func.current_timestamp()
    )
    updated_at = Column(
        TIMESTAMP, nullable=False, server_default=func.current_timestamp(), default=func.current_timestamp()
    )
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="topics")
    comments = relationship("Comment", back_populates="topic")
