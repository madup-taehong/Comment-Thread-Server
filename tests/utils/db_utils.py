from typing import Type, List

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import Base


def setup_test_data(session: Session, model: Type[Base], data: List[Base], sequence_name: str = None) -> None:
    """테스트 데이터를 넣어주는 함수"""
    # 모델 인스턴스들을 세션에 추가
    for item in data:
        # 모델의 컬럼 정보를 가져와서 새 인스턴스 생성 - 그냥 넣으면 반복하는 테스트에서 제대로 추가를 못해서 에러 발생
        columns = {c.name: getattr(item, c.name) for c in model.__table__.columns}
        new_item = model(**columns)
        session.add(new_item)
    session.commit()

    # 시퀀스 업데이트 (필요한 경우)
    if sequence_name:
        session.execute(text(f"SELECT setval('{sequence_name}', (SELECT MAX(id) FROM {model.__table__.name}))"))
        session.commit()


def cleanup_test_data(session: Session, model: Type[Base], schema_name: str = None) -> None:
    """테스트 데이터를 초기화 하는 함수"""
    session.query(model).delete()
    session.commit()
