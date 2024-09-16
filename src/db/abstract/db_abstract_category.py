from abc import ABC, abstractmethod


class AbstractCategoryDatabase(ABC):
    """Abstract class for interacting with Categories in the database."""

    @abstractmethod
    def get_all_categories(self, db, pagination):
        """Retrieve all Categories from database with pagination support."""
        pass

    @abstractmethod
    def get_category_by_id(self, db, category_id):
        """Retrieve Category by ID from database."""
        pass

    @abstractmethod
    def get_category_by_name(self, db, category_name):
        """Retrieve Category by name from database."""
        pass

    @abstractmethod
    def create_category(self, db, category):
        """Create new Category in database."""
        pass

    @abstractmethod
    def remove_category(self, db, category_id):
        """Remove Category by ID from database."""
        pass

    @abstractmethod
    def update_category(self, db, category_id, category_data):
        """Update Category by ID in database."""
        pass

    @abstractmethod
    def get_category_relations(self, db, category_id):
        """Retrieve all Categories related to specific category."""
        pass

