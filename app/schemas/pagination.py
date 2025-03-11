from pydantic import BaseModel, Field
from typing import Optional, Generic, TypeVar, List

T = TypeVar("T")


class PaginationParams(BaseModel):
    page_index: Optional[int] = 0
    page_size: Optional[int] = 20

    cursor: Optional[int] = None
    limit: Optional[int] = 20


class PaginationResponse(BaseModel, Generic[T]):
    items: List[T]
    total_count: int
    total_page: int
    current_page: int


class CursorResponse(BaseModel, Generic[T]):
    items: List[T]
    next_cursor: Optional[int] = None
    prev_cursor: Optional[int] = None
    limit: int = 20
