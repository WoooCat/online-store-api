from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db.sqlalchemy_db.db_category import SqlalchemyCategoryDatabase
from ..services.category_service import CategoryService
from ..schemas.category_schemes import CategoryCreate, Category, CategoryUpdate
from ..db.database import get_db
from ..request_utils import PaginationParams


router = APIRouter(
    prefix="/category",
    tags=["category"],
)


category_service = CategoryService(db=SqlalchemyCategoryDatabase())


@router.get("/", response_model=List[Category])
def get_categories(db: Session = Depends(get_db), pagination: PaginationParams = Depends()) -> List[Category]:
    """Get all Categories endpoint."""
    return category_service.get_categories(db, pagination)


@router.post("/")
def create_category(request: CategoryCreate, db: Session = Depends(get_db)) -> Category:
    """
    Create new Category endpoint.

    If `parent_id` is provided as `0`, it will be ignored, as it is meant to be used only for subcategories.
    """
    return category_service.create_category(db, request)


@router.get("/id/{category_id}", response_model=Category)
def get_category_by_id(category_id: int, db: Session = Depends(get_db)) -> Category:
    """Get Category by ID endpoint"""
    return category_service.get_category_by_id(category_id, db)


@router.get("/name/{name}", response_model=Category)
def get_category_by_name(name: str, db: Session = Depends(get_db)) -> Category:
    """Get Category by Name endpoint"""
    return category_service.get_category_by_name(name, db)


@router.patch("/{id}", response_model=Category)
def update_category(request: CategoryUpdate, category_id: int, db: Session = Depends(get_db)) -> Category:
    """Update Category by ID endpoint"""
    return category_service.update_category(db, category_id, request)


@router.delete('/delete/{category_id}')
def remove_category(category_id: int, db: Session = Depends(get_db)) -> Category:
    """Delete Category by ID endpoint"""
    return category_service.remove_category(db, category_id)
