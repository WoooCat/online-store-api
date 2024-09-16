from typing import Dict, List

from sqlalchemy.orm import Session

from ...db.models import DbCategory, DbCategoryRelation, DbProduct
from ...enums import FilterField
from ...request_utils import PaginationParams, apply_pagination, get_object_or_404
from ...schemas.product_schemes import ProductCreate, ProductUpdate
from ..abstract.db_abstract_product import AbstractProductDatabase


class SqlalchemyProductDatabase(AbstractProductDatabase):
    """SQLAlchemy implementation of the AbstractCategoryDatabase for managing Products in the database."""

    def get_all_products(self, db: Session, pagination: PaginationParams) -> List[DbProduct]:
        """Get all Products from the database with pagination support."""
        db_products = db.query(DbProduct).filter(DbProduct.stock > 0)
        return apply_pagination(db_products, pagination)

    def create_product(self, db: Session, product: ProductCreate) -> DbProduct:
        """Create new Product in the database."""
        get_object_or_404(DbCategory, FilterField.ID, product.category_id, db)
        db_product = DbProduct(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    def get_product_by_id(self, db: Session, product_id: int) -> DbProduct:
        """Get Product by ID from the database."""
        return get_object_or_404(DbProduct, FilterField.ID, product_id, db)

    def get_product_by_name(self, db: Session, product_name: str) -> DbProduct:
        """Get Product by name from the database."""
        return get_object_or_404(DbProduct, FilterField.NAME, product_name, db)

    def get_products_by_category(self, db: Session, category_id: int, pagination: PaginationParams) -> List[DbProduct]:
        """Get all Products in specific Category and its Subcategories."""
        all_categories = self._get_all_subcategories(db, category_id)
        all_categories.append(category_id)
        db_products = db.query(DbProduct).filter(DbProduct.category_id.in_(all_categories), DbProduct.stock > 0)
        return apply_pagination(db_products, pagination)

    def update_product(self, db: Session, product_id: int, product_data: ProductUpdate) -> DbProduct:
        """Update Product by ID in the database."""
        db_product = get_object_or_404(DbProduct, FilterField.ID, product_id, db)
        get_object_or_404(DbCategory, FilterField.ID, product_data.category_id, db)
        for key, value in product_data.dict(exclude_unset=True).items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
        return db_product

    def update_product_price(self, db: Session, product_id: int, new_price: float) -> DbProduct:
        """Update price of Product by ID in database."""
        db_product = get_object_or_404(DbProduct, FilterField.ID, product_id, db)
        db_product.price = new_price
        db.commit()
        db.refresh(db_product)
        return db_product

    def remove_product(self, db: Session, product_id: int) -> Dict:
        """Remove Product by ID from the database."""
        db_product = get_object_or_404(DbProduct, FilterField.ID, product_id, db)

        db.delete(db_product)
        db.commit()
        return {'message': "Product deleted successfully"}

    def _get_all_subcategories(self, db: Session, category_id: int) -> List[int]:
        """Get all Subcategories for given Category ID."""
        subcategories = db.query(DbCategoryRelation).filter(DbCategoryRelation.ancestor_id == category_id).all()
        return [relation.descendant_id for relation in subcategories]
