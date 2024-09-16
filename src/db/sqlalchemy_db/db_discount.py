from decimal import Decimal
from typing import List, Dict
from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..abstract.db_abstract_doscount import AbstractDiscountDatabase
from ...db.models import DbDiscount, DbProductDiscount, DbProduct
from ...enums import FilterField
from ...schemas.discount_schemes import DiscountCreate, DiscountUpdate
from ...request_utils import get_object_or_404, PaginationParams, apply_pagination


class SqlalchemyDiscountDatabase(AbstractDiscountDatabase):
    """SQLAlchemy implementation of the AbstractDiscountDatabase for managing Discounts in the database."""

    def get_all_discounts(self, db: Session, pagination: PaginationParams) -> List[DbDiscount]:
        """Get all Discounts from the database with pagination support."""
        db_discounts = db.query(DbDiscount)
        return apply_pagination(db_discounts, pagination)

    def create_discount(self, db: Session, discount: DiscountCreate) -> DbDiscount:
        """Create new Discount in the database."""
        db_discount = DbDiscount(**discount.dict())
        db.add(db_discount)
        db.commit()
        db.refresh(db_discount)
        return db_discount

    def get_discount_by_id(self, db: Session, discount_id: int) -> DbDiscount:
        """Get Discount by ID from the database."""
        return get_object_or_404(DbDiscount, FilterField.ID, discount_id, db)

    def update_discount(self, db: Session, discount_id: int, discount_update: DiscountUpdate) -> DbDiscount:
        """Update existing Discount by ID in the database."""
        db_discount = get_object_or_404(DbDiscount, FilterField.ID, discount_id, db)
        for key, value in discount_update.dict(exclude_unset=True).items():
            setattr(db_discount, key, value)
        db.commit()
        db.refresh(db_discount)
        return db_discount

    def delete_discount(self, db: Session, discount_id: int) -> DbDiscount:
        """Delete existing Discount by ID from the database."""
        db_discount = get_object_or_404(DbDiscount, FilterField.ID, discount_id, db)
        db.delete(db_discount)
        db.commit()
        return db_discount

    def add_discount_to_product(self, db: Session, product_id: int, discount_id: int) -> DbProduct:
        """Add Discount to Product and update Product price."""
        try:
            db.begin()
            db_product_discount = DbProductDiscount(product_id=product_id, discount_id=discount_id)
            db.add(db_product_discount)
            db_product = get_object_or_404(DbProduct, FilterField.ID, product_id, db)
            db_discount = get_object_or_404(DbDiscount, FilterField.ID, discount_id, db)

            # Convert price and discount percentage to Decimal
            price = Decimal(db_product.price)
            percentage = Decimal(db_discount.percentage)
            # Update the product price based on the discount
            new_price = price * (Decimal('1.00') - (percentage / Decimal('100.00')))
            db_product.price = float(new_price)

            db.commit()
            db.refresh(db_product)
            db.refresh(db_product_discount)
            return db_product
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to add Discount: {str(e)}")

    def remove_discount_from_product(self, db: Session, product_id: int, discount_id: int) -> DbProduct:
        """Remove Discount from Product and update Product price."""
        try:
            db_product_discount = db.query(DbProductDiscount).filter(
                DbProductDiscount.product_id == product_id,
                DbProductDiscount.discount_id == discount_id
            ).first()

            if not db_product_discount:
                raise HTTPException(
                    status_code=404,
                    detail=f"Product Discount with 'product_id': {product_id} and 'discount_id': {discount_id} not found"
                )

            db_product = get_object_or_404(DbProduct, FilterField.ID, product_id, db)
            # Convert price and percentage to Decimal
            price = Decimal(db_product.price)
            percentage = Decimal(db_product_discount.discount.percentage)
            # Calculate the original price before discount
            original_price = price / (Decimal('1.00') - percentage / Decimal('100.00'))
            db_product.price = float(original_price)

            db.delete(db_product_discount)
            db.commit()
            db.refresh(db_product)
            return db_product
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to remove Discount: {str(e)}")
