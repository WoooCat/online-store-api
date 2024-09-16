from typing import Dict, List

from sqlalchemy.orm import Session

from ..db.abstract.db_abstract_product import AbstractProductDatabase
from ..request_utils import PaginationParams
from ..schemas.product_schemes import Product, ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, db: AbstractProductDatabase):
        """Initialize ProductService with database instance."""
        self.db = db

    def get_products(self, db: Session, pagination: PaginationParams) -> List[Product]:
        """Get all Products with pagination support."""
        return self.db.get_all_products(db, pagination)

    def create_product(self, db: Session, product: ProductCreate) -> Product:
        """Create new Product."""
        return self.db.create_product(db, product)

    def get_product_by_id(self, db: Session, product_id: int) -> Product:
        """Get Product by ID."""
        return self.db.get_product_by_id(db, product_id)

    def get_product_by_name(self, db: Session, product_name: str) -> Product:
        """Get Product by name."""
        return self.db.get_product_by_name(db, product_name)

    def get_products_by_category(self, db: Session, category_id: int, pagination: PaginationParams) -> List[Product]:
        """Get all Products in specific Category and Subcategories."""
        return self.db.get_products_by_category(db, category_id, pagination)

    def update_product(self, db: Session, product_id: int, product_data: ProductUpdate) -> Product:
        """Update Product by ID."""
        return self.db.update_product(db, product_id, product_data)

    def update_product_price(self, db: Session, product_id: int, new_price: float) -> Product:
        """Update price of Product by ID."""
        return self.db.update_product_price(db, product_id, new_price)

    def remove_product(self, db: Session, product_id: int) -> Dict:
        """Remove Product by ID."""
        return self.db.remove_product(db, product_id)
