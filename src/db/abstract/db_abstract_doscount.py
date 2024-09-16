from abc import ABC, abstractmethod


class AbstractDiscountDatabase(ABC):
    """Abstract class for interacting with Discounts in the database."""

    @abstractmethod
    def get_all_discounts(self, db, pagination):
        """Get all Discounts from the database with pagination support."""
        pass

    @abstractmethod
    def create_discount(self, db, discount):
        """Create new Discount in the database."""
        pass

    @abstractmethod
    def get_discount_by_id(self, db, discount_id):
        """Get Discount by ID from the database."""
        pass

    @abstractmethod
    def update_discount(self, db, discount_id, discount_data):
        """Update existing Discount by ID in the database."""
        pass

    @abstractmethod
    def delete_discount(self, db, discount_id):
        """Delete existing Discount by ID from the database."""
        pass

    @abstractmethod
    def add_discount_to_product(self, db, product_id, discount_id):
        """Add Discount to Product and update Product price."""
        pass

    @abstractmethod
    def remove_discount_from_product(self, db, product_id, discount_id):
        """Remove Discount from Product and update Product price."""
        pass
