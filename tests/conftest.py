import os
import subprocess
import time
from asyncio import get_event_loop
from unittest.mock import MagicMock, patch

import pytest
import pytest_asyncio
from httpx import AsyncClient

from sqlalchemy_utils import create_database, database_exists

from app.db.database import SqlAlchemy, Base
from app.models import User, Topic, Comment
from app.main import create_app
from app.config import DBConnection
from tests.dummy_data.dummy_comment_data import dummy_comment_data
from tests.dummy_data.dummy_topic_data import dummy_topic_data
from tests.dummy_data.dummy_user_data import dummy_user_data
from tests.utils.db_utils import setup_test_data, cleanup_test_data

TEST_DATABASE_URL = "postgresql://test_user:test_password@localhost:5433/test_db"

_test_db = None


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def docker_compose_file():
    """Docker compose 파일 경로를 반환합니다."""
    print(os.path.dirname(__file__), __file__)
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "docker-compose.test.yml")


@pytest.fixture(scope="session", autouse=True)
def docker_services(docker_compose_file):
    """테스트용 도커 실행"""

    # docker-compose 실행
    subprocess.run(["docker-compose", "-f", docker_compose_file, "up", "-d"], check=True)

    # DB가 준비될 때까지 대기
    max_retries = 30
    retry_interval = 1
    for _ in range(max_retries):
        try:
            # Docker 컨테이너 상태 확인
            result = subprocess.run(
                ["docker", "container", "inspect", "-f", "{{.State.Health.Status}}", "comment-thread-server-test-db-1"],
                check=True,
                capture_output=True,
                text=True,
            )
            if result.stdout.strip() == "healthy":
                break
            time.sleep(retry_interval)
        except subprocess.CalledProcessError:
            time.sleep(retry_interval)
    else:
        raise Exception("Database failed to start")

    yield

    # 테스트 종료 후 Docker 컨테이너 종료
    subprocess.run(["docker-compose", "-f", docker_compose_file, "down"], check=True)


async def _set_up_test_db():
    """
    테스트 DB 세팅
    :return:
    """
    db = SqlAlchemy(Base)
    db.init_db(database_info=DBConnection(SQLALCHEMY_DATABASE_URL=TEST_DATABASE_URL))
    Base.metadata.create_all(db.engine())
    sess = db.session()
    sess.commit()
    return db


@pytest_asyncio.fixture(scope="session")
async def db():
    """테스트 DB 세팅"""
    # DB 연결 정보 설정
    db = SqlAlchemy(Base)
    db.init_db(database_info=DBConnection(SQLALCHEMY_DATABASE_URL=TEST_DATABASE_URL))

    # 테스트 DB가 없다면 생성
    if not database_exists(TEST_DATABASE_URL):
        create_database(TEST_DATABASE_URL)

    # 테스트 DB 테이블 생성
    Base.metadata.create_all(db.engine())

    yield db


@pytest_asyncio.fixture(scope="session")
async def client():
    """
    서버 생성 함수
    :return:
    """
    global _test_db
    _test_db = await _set_up_test_db()
    app = create_app()
    async with AsyncClient(app=app, base_url="http://localhost:8000") as client:
        yield client


@pytest_asyncio.fixture
def session():
    global _test_db
    session = _test_db.session()
    yield session


@pytest_asyncio.fixture
async def setup_user_data(session):
    """유저 데이터를 설정하는 fixture"""
    setup_test_data(session=session, model=User, data=dummy_user_data, sequence_name="users_id_seq")
    yield
    cleanup_test_data(session, User)


@pytest_asyncio.fixture
async def setup_topic_data(session, setup_user_data):
    """댓글 데이터를 설정하는 fixture"""
    setup_test_data(session=session, model=Topic, data=dummy_topic_data, sequence_name="topics_id_seq")
    setup_test_data(session=session, model=Comment, data=dummy_comment_data, sequence_name="comments_id_seq")
    yield
    cleanup_test_data(session, Comment)
    cleanup_test_data(session, Topic)
