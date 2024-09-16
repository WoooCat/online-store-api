from typing import List
from sqlalchemy.orm import Session
from ..abstract.db_abstract_category import AbstractCategoryDatabase
from ..models import DbCategory, DbCategoryRelation
from ...enums import FilterField
from ...schemas.category_schemes import CategoryCreate, CategoryUpdate
from ...request_utils import apply_pagination, PaginationParams, get_object_or_404


class SqlalchemyCategoryDatabase(AbstractCategoryDatabase):
    """SQLAlchemy implementation of the AbstractCategoryDatabase for managing Categories in the database."""

    def get_all_categories(self, db: Session, pagination: PaginationParams) -> List[DbCategory]:
        """Retrieve all categories from the database with pagination."""
        db_categories = db.query(DbCategory)
        return apply_pagination(db_categories, pagination)

    def get_category_by_id(self, category_id: int, db: Session) -> DbCategory:
        """Retrieve a category by its ID."""
        return get_object_or_404(DbCategory, FilterField.ID, category_id, db)

    def get_category_by_name(self, category_name: str, db: Session) -> DbCategory:
        """Retrieve a category by its name."""
        return get_object_or_404(DbCategory, FilterField.NAME, category_name, db)

    def update_category(self, db: Session, category_id: int, category_data: CategoryUpdate) -> DbCategory:
        """Update a category's details."""
        db_category = get_object_or_404(DbCategory, FilterField.ID, category_id, db)

        if db_category:
            for key, value in category_data.dict(exclude_unset=True).items():
                setattr(db_category, key, value)
            db.commit()
            db.refresh(db_category)

        return db_category

    def create_category(self, db: Session, category: CategoryCreate) -> DbCategory:
        """Create a new category and manage category relations."""
        new_category = DbCategory(name=category.name, parent_id=category.parent_id)
        db.add(new_category)
        db.commit()

        if category.parent_id:
            self._update_category_relations(db, new_category, category.parent_id)
        self._add_self_relation(db, new_category)

        db.commit()
        db.refresh(new_category)
        return new_category

    def remove_category(self, db: Session, category_id: int) -> DbCategory:
        """Remove a category by its ID and its relations."""
        db_category = get_object_or_404(DbCategory, FilterField.ID, category_id, db)
        self._remove_category_relations(db, category_id)
        db.delete(db_category)
        db.commit()
        return db_category

    def _update_category_relations(self, db: Session, new_category: DbCategory, parent_id: int) -> None:
        """Update relations for the newly created category based on its parent."""
        relations = db.query(DbCategoryRelation).filter_by(descendant_id=parent_id).all()
        for relation in relations:
            new_relation = DbCategoryRelation(
                ancestor_id=relation.ancestor_id,
                descendant_id=new_category.id,
                depth=relation.depth + 1
            )
            db.add(new_relation)
        db.add(DbCategoryRelation(
            ancestor_id=parent_id,
            descendant_id=new_category.id,
            depth=1
        ))

    def _add_self_relation(self, db: Session, new_category: DbCategory) -> None:
        """Add a self-relation for the newly created category."""
        db.add(DbCategoryRelation(
            ancestor_id=new_category.id,
            descendant_id=new_category.id,
            depth=0
        ))

    def _remove_category_relations(self, db: Session, category_id: int) -> None:
        """Remove all relations associated with the category."""
        db.query(DbCategoryRelation).filter(
            (DbCategoryRelation.ancestor_id == category_id) |
            (DbCategoryRelation.descendant_id == category_id)
        ).delete(synchronize_session=False)

    def get_category_relations(self, db: Session, category_id: int) -> List[DbCategory]:
        """Retrieve all categories related to a given category (subcategories)."""
        relations = db.query(DbCategoryRelation).filter(DbCategoryRelation.ancestor_id == category_id).all()
        related_category_ids = [relation.descendant_id for relation in relations]
        return db.query(DbCategory).filter(DbCategory.id.in_(related_category_ids)).all()
