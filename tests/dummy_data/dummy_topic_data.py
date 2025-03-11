from app.models import Topic

dummy_topic_data = [
    Topic(
        id=1,
        title="토픽1",
        content="토픽1 콘텐츠",
        user_id=1,
    ),
    Topic(
        id=2,
        title="토픽2",
        content="토픽2 콘텐츠",
        user_id=2,
    ),
    Topic(
        id=3,
        title="토픽3",
        content="토픽3 콘텐츠",
        user_id=1,
    ),
]
