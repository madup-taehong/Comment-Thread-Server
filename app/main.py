from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from app.config import settings

from app.api.comment import comment_router
from app.api.topic import topic_router
from app.api.auth import auth_router
from app.api.user import user_router

from app.db.database import db


def create_app():
    fastapi_app = FastAPI()

    db.init_db(database_info=settings.DB_INFOS)
    db.init_app_event(app=fastapi_app)

    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @fastapi_app.get("/")
    def read_root():
        return {"status": "ok"}

    fastapi_app.include_router(auth_router)
    fastapi_app.include_router(user_router)
    fastapi_app.include_router(comment_router)
    fastapi_app.include_router(topic_router)

    return fastapi_app


if __name__ == "__main__":
    uvicorn.run(create_app, host="0.0.0.0", port=8000)
    # NOTE: 기존 코드 카피하더라도 사용하는 이유 알아야 됌.
    # NOTE: 중복되는 검증 로직은 별도의 depends를 모아놓는 곳에서 관리하면 코드 파악 용이
    # NOTE: 함수 인풋, 아웃풋 typing 적어주면 코드 가독성 증가
