from datetime import timedelta

import pytest
from app.utils.jwt import create_access_token


@pytest.mark.asyncio
async def test_get_topics(client, setup_topic_data):
    """토픽 목록 조회 API 테스트"""
    response = await client.get("/v1/topics")
    # 성공적으로 조회되고 데이터는 3개
    assert response.status_code == 200
    data = response.json()
    assert data.get("total_count") == 3


@pytest.mark.asyncio
async def test_get_topic_by_id(client, setup_topic_data):
    """특정 토픽 조회 API 테스트"""
    response = await client.get("/v1/topics/1")
    # 성공적으로 조회되고 내용 확인
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "토픽1"


@pytest.mark.asyncio
async def test_create_topic(client, setup_topic_data):
    """토픽 생성 API 테스트"""

    new_topic = {"title": "새로운 토픽", "content": "새로운 토픽 콘텐츠"}
    response = await client.post(
        "/v1/topics",
        json=new_topic,
    )
    assert response.status_code == 401

    access_token = create_access_token(data={"email": "test@test.com"}, expires_delta=timedelta(minutes=30))

    response = await client.post("/v1/topics", json=new_topic, headers={"Authorization": f"Bearer {access_token}"})

    # 정상적으로 조회되고 내용 확인
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "새로운 토픽"
    assert data["content"] == "새로운 토픽 콘텐츠"
