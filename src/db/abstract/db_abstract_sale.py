from abc import ABC, abstractmethod


class AbstractSaleDatabase(ABC):
    """Abstract class for interacting with Sales in the database."""

    @abstractmethod
    def sell_product(self, db, product_id, quantity):
        """Sell Product, decrease stock and create Sale record in the database."""
        pass

    @abstractmethod
    def get_sales_report(self, db, pagination, category_id, product_id):
        """Get Sales report, optionally filtered by Category or Product."""
        pass
