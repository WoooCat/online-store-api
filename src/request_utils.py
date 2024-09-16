from fastapi import HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.enums import FilterField


class PaginationParams:
    def __init__(
            self,
            limit: int = Query(10, ge=1, description="Number of items to return"),
            offset: int = Query(0, ge=0, description="Number of items to return")
    ):
        self.limit = limit
        self.offset = offset


def apply_pagination(query: Query, pagination: PaginationParams):
    """Apply pagination to a SQLAlchemy query using PaginationParams."""
    return query.limit(pagination.limit).offset(pagination.offset).all()


def get_object_or_404(model, field: FilterField, value: any, db: Session = Depends(get_db)):
    """
    FastAPI dependency to fetch an object by any field or raise 404 if not found.

    Return:
        Object instance if found, raises 404 HTTPException otherwise
    """
    obj = db.query(model).filter(getattr(model, field.value) == value).first()
    if not obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__name__} with '{field.value}': '{value}' not found"
        )
    return obj
