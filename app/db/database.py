from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class SqlAlchemy:
    def __init__(self, base_class):
        self._engine = None
        self._session = None
        self.Base = base_class

    @staticmethod
    def create_engine(info):
        engine = create_engine(
            url=info.SQLALCHEMY_DATABASE_URL,
            echo=True,
        )
        return engine

    @staticmethod
    def create_session_maker(engine: Engine):
        """
        DB 세션 만드는 함수.
        """
        session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return session_local

    def init_app_event(self, app: FastAPI):
        @app.on_event("startup")
        def startup():
            self._engine.connect()

        @app.on_event("shutdown")
        def shutdown():
            self.close_db()

    def init_db(self, database_info):
        """
        DB 초기화 함수
        :param database_info: DB 연결 정보
        :return:
        """
        if not database_info:
            raise Exception("DB 연결 정보가 없습니다.")
        else:
            self._engine = self.create_engine(info=database_info)
            self._session = self.create_session_maker(engine=self._engine)

    def session(self):
        return self._session()

    def engine(self):
        return self._engine

    def close_db(self):
        self._engine.dispose()


db = SqlAlchemy(Base)
