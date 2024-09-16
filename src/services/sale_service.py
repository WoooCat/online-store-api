from typing import Optional, List
from sqlalchemy.orm import Session
from ..db.abstract.db_abstract_sale import AbstractSaleDatabase
from ..db.models import DbSale
from ..request_utils import PaginationParams


class SaleService:
    def __init__(self, db: AbstractSaleDatabase):
        """Initialize SaleService with database instance."""
        self.db = db

    def sell_product(self, db: Session, product_id: int, quantity: int) -> DbSale:
        """Sell Product, decrease stock and create Sale record in the database."""
        return self.db.sell_product(db, product_id, quantity)

    def get_sales_report(
            self,
            db: Session,
            pagination: PaginationParams,
            category_id: Optional[int] = None,
            product_id: Optional[int] = None,
    ) -> List[DbSale]:
        """Get Sales report, optionally filtered by Category or Product."""
        return self.db.get_sales_report(db, pagination, category_id, product_id)
