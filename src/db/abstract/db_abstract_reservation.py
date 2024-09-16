from abc import ABC, abstractmethod


class AbstractReservationDatabase(ABC):
    """Abstract class for interacting with Reservations in the database."""

    @abstractmethod
    def get_reservations(self, db, pagination):
        """Get all Reservations from the database."""
        pass

    @abstractmethod
    def get_active_reservations(self, db, pagination):
        """Get active Reservations from the database."""
        pass

    @abstractmethod
    def get_reservation_by_id(self, db, reservation_id):
        """Get Reservation by ID from the database."""
        pass

    @abstractmethod
    def reserve_product(self, db, product_id, quantity):
        """Reserve Product by ID in the database."""
        pass

    @abstractmethod
    def cancel_reservation(self, db, reservation_id):
        """Cancel Reservation by ID in the database."""
        pass
