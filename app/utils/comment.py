from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.models.user import User


def get_comment_tree(db: Session, topic_id: int, parent_id=None, depth=0, max_depth=2):
    """
    코멘트 트리를 만들어주는 함수
    """
    # 해당하는 parent_id을 가지는 코멘트 조회
    comments = (
        db.query(Comment)
        .filter(Comment.topic_id == topic_id, Comment.parent_id == parent_id)
        .order_by(Comment.created_at.asc())
        .all()
    )

    # 댓글이 있는 경우에 순회하며 사용자 정보와 대댓글 정보 추가
    for comment in comments:
        # 사용자 정보 포함
        comment.user = db.query(User).filter(User.id == comment.user_id).first()

        # 최대 깊이에 도달하지 않은 경우 자식 코멘트 조회
        if depth < max_depth:
            comment.replies = get_comment_tree(db, topic_id, comment.id, depth + 1, max_depth)
        else:
            comment.replies = []

    return comments
