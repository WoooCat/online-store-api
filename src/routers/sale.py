from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..db.sqlalchemy_db.db_sail import SqlalchemySaleDatabase
from ..request_utils import PaginationParams
from ..schemas.sale_schemes import Sale
from ..services.sale_service import SaleService

router = APIRouter(
    prefix="/sale",
    tags=["sale"],
)

sell_service = SaleService(db=SqlalchemySaleDatabase())


@router.post("/product_id/{product_id}", response_model=Sale)
def sell_product(product_id: int, quantity: int, db: Session = Depends(get_db)) -> Sale:
    return sell_service.sell_product(db, product_id, quantity)


@router.get("/sales/report", response_model=List[Sale])
def get_sales_report(
    category_id: Optional[int] = None,
    product_id: Optional[int] = None,
    pagination: PaginationParams = Depends(),
    db: Session = Depends(get_db),
) -> List[Sale]:
    """Get sales report, optionally filtered by category or product."""
    return sell_service.get_sales_report(db, pagination, category_id, product_id)
