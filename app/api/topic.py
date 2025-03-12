from fastapi import APIRouter, Depends, HTTPException, status
from typing import Union

from sqlalchemy.orm import Session

from app.utils.jwt import get_current_user
from app.utils.comment import get_comment_tree
from app.config import settings
from app.db.database import db
from app.models.topic import Topic
from app.models.user import User
from app.schemas.topic import TopicCreate, TopicResponse
from app.schemas.pagination import PaginationParams, PaginationResponse, CursorResponse

topic_router = APIRouter(prefix=f"{settings.API_VERSION}/topics", tags=["Topics"])


@topic_router.post("", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
def create_topic(topic_data: TopicCreate, current_user: User = Depends(get_current_user)):
    """
    토픽 생성 api

    input:
        topic_data: 토픽 생성 데이터
        current_user: 현재 인증된 사용자(로그인 필요)

    output:
        TopicResponse: 생성된 토픽 정보
    """
    with db.session() as session:
        new_topic = Topic(title=topic_data.title, content=topic_data.content, user_id=current_user.id)

        session.add(new_topic)
        session.commit()
        session.refresh(new_topic)

        return TopicResponse.from_orm(new_topic)


@topic_router.get("", response_model=Union[PaginationResponse[TopicResponse], CursorResponse[TopicResponse]])
def get_topics(pagination: PaginationParams = Depends()):
    """
    토픽 조회 api

    input:
        pagination: 페이지네이션관련 파라미터

    output:
        Union[PaginationResponse[TopicResponse], CursorResponse[TopicResponse]]:
            - 커서가 있는 경우: 커서 기반 페이지네이션 응답
            - 커서가 없는 경우: 오프셋 기반 페이지네이션 응답
    """
    with db.session() as session:
        # 커서가 있는 경우 커서 기반으로 페이지네이션
        if pagination.cursor is not None:
            query = session.query(Topic).order_by(Topic.id)

            if pagination.cursor > 0:
                query = query.filter(Topic.id >= pagination.cursor)

            # limit보다 하나 더 조회 (나중에 next_cursor를 넣어주기 위함)
            items = query.limit(pagination.limit + 1).all()

            has_next = len(items) > pagination.limit
            next_cursor = None
            # 다음 목록이 있다면 마지막 아이디를 next_cursor로 넣어주고 배열에서 제외
            if has_next:
                next_cursor = items[-1].id
                items = items[:-1]

            prev_cursor = pagination.cursor

            # 아이템별로 코멘트 트리 추가
            for item in items:
                item.comments = get_comment_tree(session, item.id)

            return CursorResponse(items=items, next_cursor=next_cursor, prev_cursor=prev_cursor, limit=pagination.limit)

        # 아닌경우 offset 기반으로 페이지네이션
        else:
            total_count = session.query(Topic).count()
            skip = pagination.page_index * pagination.page_size

            items = session.query(Topic).order_by(Topic.id.desc()).offset(skip).limit(pagination.page_size).all()

            # 아이템별로 코멘트 트리 추가
            for item in items:
                item.comments = get_comment_tree(session, item.id)

            total_page = (total_count + pagination.page_size - 1) // pagination.page_size

            return PaginationResponse(
                items=items, total_count=total_count, total_page=total_page, current_page=pagination.page_index
            )


@topic_router.get("/{topic_id}", response_model=TopicResponse)
def get_topic(topic_id: int):
    """
    타겟 토픽 조회

    input:
        topic_id: 조회할 토픽의 ID

    output:
        TopicResponse: 조회된 토픽 정보

    error:
        토픽이 존재하지 않는 경우 404 에러 발생
    """
    with db.session() as session:
        topic = session.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="주제를 찾을 수 없습니다")

        topic.user = session.query(User).filter(User.id == topic.user_id).first()

        # 댓글 트리 생성
        topic.comments = get_comment_tree(session, topic_id)

        return TopicResponse.from_orm(topic)
