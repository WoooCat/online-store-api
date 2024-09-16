from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db.sqlalchemy_db.db_discount import SqlalchemyDiscountDatabase
from ..schemas.discount_schemes import DiscountCreate, DiscountUpdate, Discount
from ..schemas.product_schemes import Product
from ..services.discount_service import DiscountService
from ..db.database import get_db
from ..request_utils import PaginationParams

router = APIRouter(
    prefix="/discount",
    tags=["discount"],
)

discount_service = DiscountService(db=SqlalchemyDiscountDatabase())


@router.post("/create", response_model=Discount)
def create_discount(discount: DiscountCreate, db: Session = Depends(get_db)) -> Discount:
    """Create Discount endpoint."""
    return discount_service.create_discount(db, discount)


@router.get("/discounts", response_model=List[Discount])
def get_discounts(db: Session = Depends(get_db), pagination: PaginationParams = Depends()) -> List[Discount]:
    """Get all Discounts endpoint."""
    return discount_service.get_discounts(db, pagination)


@router.get("/id/{discount_id}", response_model=Discount)
def get_discount(discount_id: int, db: Session = Depends(get_db)) -> Discount:
    """Get Discount by ID endpoint."""
    return discount_service.get_discount_by_id(db, discount_id)


@router.patch("/{discount_id}", response_model=Discount)
def update_discount(discount_id: int, discount: DiscountUpdate, db: Session = Depends(get_db)) -> Discount:
    """Update Discount by ID endpoint."""
    return discount_service.update_discount(db, discount_id, discount)


@router.delete("/{discount_id}", response_model=Discount)
def delete_discount(discount_id: int, db: Session = Depends(get_db)) -> Discount:
    """Delete Discount by ID endpoint."""
    return discount_service.delete_discount(db, discount_id)


@router.post("/product/{product_id}/discount/{discount_id}", response_model=Product)
def add_discount_to_product(product_id: int, discount_id: int, db: Session = Depends(get_db)) -> Discount:
    """Add Discount to Product by ID endpoint."""
    return discount_service.add_discount_to_product(db, product_id, discount_id)


@router.delete("/product/{product_id}/discount/{discount_id}", response_model=Product)
def remove_discount_from_product(product_id: int, discount_id: int, db: Session = Depends(get_db)) -> Discount:
    """Remove Discount from Product by ID endpoint."""
    return discount_service.remove_discount_from_product(db, product_id, discount_id)
