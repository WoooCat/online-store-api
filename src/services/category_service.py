from typing import List
from sqlalchemy.orm import Session
from ..db.sqlalchemy_db.db_category import SqlalchemyCategoryDatabase
from ..schemas.category_schemes import CategoryCreate, CategoryUpdate, Category
from ..request_utils import PaginationParams


class CategoryService:
    """Service class for managing Categories, using an Abstract Category database implementation."""

    def __init__(self, db: SqlalchemyCategoryDatabase):
        """Initialize the CategoryService with the provided database implementation."""
        self.db = db

    def get_categories(self, db: Session, pagination: PaginationParams) -> List[Category]:
        """Get all Categories with pagination."""
        return self.db.get_all_categories(db, pagination)

    def get_category_by_id(self, category_id: int, db: Session) -> Category:
        """Get Category by ID."""
        return self.db.get_category_by_id(category_id, db)

    def get_category_by_name(self, name: str, db: Session) -> Category:
        """Get Category by name."""
        return self.db.get_category_by_name(name, db)

    def update_category(self, db: Session, category_id: int, category_data: CategoryUpdate) -> Category:
        """Update Category by ID with the provided data."""
        return self.db.update_category(db, category_id, category_data)

    def create_category(self, db: Session, category: CategoryCreate) -> Category:
        """Create new Category with the provided data."""
        return self.db.create_category(db, category)

    def remove_category(self, db: Session, category_id: int) -> Category:
        """Get Category by ID."""
        return self.db.remove_category(db, category_id)

    def get_category_relations(self, db: Session, category_id: int) -> List[Category]:
        """Get all related Categories for given Category."""
        related_db_categories = self.db.get_category_relations(db, category_id)
        return related_db_categories
