from datetime import datetime

from app.models import Comment

dummy_comment_data = [
    Comment(
        id=1,
        content="첫 번째 댓글",
        user_id=1,
        topic_id=1,
        depth=0,
    ),
    Comment(id=2, content="두 번째 댓글", user_id=1, topic_id=1),
    Comment(id=3, content="첫번째 댓글의 답글", user_id=1, topic_id=1, parent_id=1, depth=1),
    Comment(id=4, content="첫번째 댓글의 두번째 답글", user_id=1, topic_id=1, parent_id=3, depth=2),
]
