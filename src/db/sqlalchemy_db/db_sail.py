from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ...db.models import DbCategory, DbProduct, DbSale
from ...enums import FilterField
from ...request_utils import PaginationParams, apply_pagination, get_object_or_404
from ..abstract.db_abstract_sale import AbstractSaleDatabase


class SqlalchemySaleDatabase(AbstractSaleDatabase):
    """SQLAlchemy implementation of the AbstractSaleDatabase for managing Sales in the database."""

    def sell_product(self, db: Session, product_id: int, quantity: int) -> DbSale:
        """Sell Product, decrease stock and create Sale record in the database."""
        db_product = get_object_or_404(DbProduct, FilterField.ID, product_id, db)
        if not db_product or db_product.stock < quantity:
            raise HTTPException(status_code=400, detail="Not enough stock")

        db_product.stock -= quantity
        sale_price = db_product.price

        db_sale = DbSale(product_id=product_id, quantity=quantity, sale_price=sale_price)
        db.add(db_sale)
        db.commit()
        db.refresh(db_sale)
        return db_sale

    def get_sales_report(
            self,
            db: Session,
            pagination: PaginationParams,
            category_id: Optional[int] = None,
            product_id: Optional[int] = None,
    ) -> List[DbSale]:
        """Get Sales report, optionally filtered by Category or Product."""
        query = db.query(DbSale).join(DbProduct)
        if category_id:
            get_object_or_404(DbCategory, FilterField.ID, category_id, db)
            query = query.filter(DbProduct.category_id == category_id)

        if product_id:
            get_object_or_404(DbProduct, FilterField.ID, product_id, db)
            query = query.filter(DbProduct.id == product_id)

        return apply_pagination(query, pagination)
