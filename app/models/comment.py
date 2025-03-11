from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(
        TIMESTAMP, nullable=False, server_default=func.current_timestamp(), default=func.current_timestamp()
    )
    updated_at = Column(
        TIMESTAMP, nullable=False, server_default=func.current_timestamp(), default=func.current_timestamp()
    )
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    depth = Column(Integer, default=0, nullable=False)

    user = relationship("User", back_populates="comments", lazy="subquery")
    topic = relationship("Topic", back_populates="comments")
    parent = relationship(
        "Comment",
        remote_side=[id],
    )
