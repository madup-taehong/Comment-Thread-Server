from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from app.utils.jwt import get_current_user
from app.config import settings
from app.db.database import db
from app.models.comment import Comment
from app.models.topic import Topic
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentResponse

comment_router = APIRouter(prefix=f"{settings.API_VERSION}/comments", tags=["Comments"])


@comment_router.post("", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(comment_data: CommentCreate, current_user: User = Depends(get_current_user)):
    """
    댓글 작성 api
    """
    with db.session() as session:
        topic = session.query(Topic).filter(Topic.id == comment_data.topic_id).first()
        if not topic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="토픽이 존재하지 않습니다.")

        depth = 0
        if comment_data.parent_id:
            parent_comment = session.query(Comment).filter(Comment.id == comment_data.parent_id).first()
            if not parent_comment:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="댓글이 존재하지 않습니다.")

            # depth에 1 더해주기
            depth = parent_comment.depth + 1

            # depth가 2를 넘어가면 에러처리
            if depth > 2:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="더이상 댓글을 달 수 없습니다.")

        new_comment = Comment(
            content=comment_data.content,
            topic_id=comment_data.topic_id,
            user_id=current_user.id,
            parent_id=comment_data.parent_id,
            depth=depth,
        )

        session.add(new_comment)
        session.commit()
        session.refresh(new_comment)

        return new_comment
