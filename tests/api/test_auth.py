import pytest


@pytest.mark.asyncio
async def test_login(client, setup_user_data):
    """
    로그인 테스트
    """
    # 디비에 존재하는 유저인 경우 테스트
    headers = {"content-type": "application/x-www-form-urlencoded"}
    user_data = {"username": "test@test.com", "password": "test"}
    response = await client.post(
        "/v1/auth/login",
        headers=headers,
        data=user_data,
    )
    # 정상적으로 로그인 성공
    assert response.status_code == 200

    # 존재하지 않는 유저 테스트 시
    not_exist_user_data = {"username": "not_exist_user@test.com", "password": "test"}
    not_exist_response = await client.post(
        "/v1/auth/login",
        headers=headers,
        data=not_exist_user_data,
    )
    # 404 에러
    assert not_exist_response.status_code == 404


@pytest.mark.asyncio
async def test_register(client, setup_user_data):
    """
    회원가입 테스트
    """
    # 없는 이메일로 가입 시 성공
    headers = {"content-type": "application/json"}
    user_data = {"email": "non_exist@example.com", "username": "test", "password": "test"}
    response = await client.post(
        "/v1/auth/register",
        headers=headers,
        json=user_data,
    )
    assert response.status_code == 200
    # 존재하는 유저로 회원가입 시 400 에러
    exist_user_data = {"email": "test@test.com", "username": "test", "password": "test"}
    exist_response = await client.post(
        "/v1/auth/register",
        headers=headers,
        json=exist_user_data,
    )
    assert exist_response.status_code == 400
