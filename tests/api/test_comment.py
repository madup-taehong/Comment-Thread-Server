from datetime import timedelta

import pytest
from httpx import AsyncClient
from utils.jwt import create_access_token


@pytest.mark.asyncio
async def test_create_comment(client, setup_topic_data):
    """댓글 생성 API 테스트"""

    access_token = create_access_token(data={"email": "test@test.com"}, expires_delta=timedelta(minutes=30))

    # 댓글 생성
    new_comment = {"content": "새로운 댓글입니다.", "topic_id": 1, "parent_id": None}

    response = await client.post("/v1/comments", json=new_comment, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "새로운 댓글입니다."
    assert data["topic_id"] == 1
    assert data["parent_id"] is None


@pytest.mark.asyncio
async def test_create_reply_comment(client: AsyncClient, setup_topic_data):
    """답글 생성 API 테스트"""
    access_token = create_access_token(data={"email": "test@test.com"}, expires_delta=timedelta(minutes=30))

    # 답글 생성
    new_reply = {"content": "새로운 답글", "topic_id": 1, "parent_id": 1}

    response = await client.post("/v1/comments", json=new_reply, headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "새로운 답글"
    assert data["topic_id"] == 1
    assert data["parent_id"] == 1

    # 이미 두개의 답글이 존재할 때 추가하면 에러
    depth_error_reply = {"content": "새로운 답글입니다.", "topic_id": 1, "parent_id": 4}
    depth_error_response = await client.post(
        "/v1/comments", json=depth_error_reply, headers={"Authorization": f"Bearer {access_token}"}
    )
    assert depth_error_response.status_code == 400
