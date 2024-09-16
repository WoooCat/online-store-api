from abc import ABC, abstractmethod


class AbstractProductDatabase(ABC):
    """Abstract class for interacting with Products in the database."""

    @abstractmethod
    def get_all_products(self, db, pagination):
        """Get all Products from the database with pagination support."""
        pass

    @abstractmethod
    def get_product_by_id(self, db, product_id):
        """Get product by ID from the database."""
        pass

    @abstractmethod
    def get_product_by_name(self, db, product_name):
        """Get Product by name from the database."""
        pass

    @abstractmethod
    def create_product(self, db, product):
        """Create new Product in the database."""
        pass

    @abstractmethod
    def remove_product(self, db, product_id):
        """Remove Product by ID from the database."""
        pass

    @abstractmethod
    def update_product(self, db, product_id, product_data):
        """Update Product by ID in database."""
        pass

    @abstractmethod
    def update_product_price(self, db, product_id, new_price):
        """Update price of Product by ID."""
        pass

    @abstractmethod
    def get_products_by_category(self, db, category_id, pagination):
        """Retrieve all Products in specific Category and its subcategories."""
        pass
