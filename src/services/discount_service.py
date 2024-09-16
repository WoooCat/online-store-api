from typing import List, Dict
from sqlalchemy.orm import Session
from ..db.abstract.db_abstract_doscount import AbstractDiscountDatabase
from ..schemas.discount_schemes import DiscountCreate, DiscountUpdate, Discount
from ..request_utils import PaginationParams


class DiscountService:
    def __init__(self, db: AbstractDiscountDatabase):
        """Initialize DiscountService with database instance."""
        self.db = db

    def get_discounts(self, db: Session, pagination: PaginationParams) -> List[Discount]:
        """Get all Discounts with pagination support."""
        return self.db.get_all_discounts(db, pagination)

    def create_discount(self, db: Session, discount: DiscountCreate) -> Discount:
        """Create new Discount."""
        return self.db.create_discount(db, discount)

    def get_discount_by_id(self, db: Session, discount_id: int) -> Discount:
        """Get Discount by ID."""
        return self.db.get_discount_by_id(db, discount_id)

    def update_discount(self, db: Session, discount_id: int, discount_data: DiscountUpdate) -> Discount:
        """Update Discount by ID."""
        return self.db.update_discount(db, discount_id, discount_data)

    def delete_discount(self, db: Session, discount_id: int) -> Discount:
        """Delete Discount by ID."""
        return self.db.delete_discount(db, discount_id)

    def add_discount_to_product(self, db: Session, product_id: int, discount_id: int) -> Discount:
        """Add Discount to Product and update Product price."""
        return self.db.add_discount_to_product(db, product_id, discount_id)

    def remove_discount_from_product(self, db: Session, product_id: int, discount_id: int) -> Discount:
        """Remove Discount from Product and update Product price."""
        return self.db.remove_discount_from_product(db, product_id, discount_id)
