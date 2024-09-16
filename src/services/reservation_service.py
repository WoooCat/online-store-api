from typing import Dict, List

from sqlalchemy.orm import Session

from ..db.abstract.db_abstract_reservation import AbstractReservationDatabase
from ..db.models import DbReservation
from ..request_utils import PaginationParams


class ReservationService:
    def __init__(self, db: AbstractReservationDatabase):
        """Initialize ReservationService with database instance."""
        self.db = db

    def get_reservations(self, db: Session, pagination: PaginationParams) -> List[DbReservation]:
        """Get all Reservations with pagination support."""
        return self.db.get_reservations(db, pagination)

    def get_active_reservations(self, db: Session, pagination: PaginationParams) -> List[DbReservation]:
        """Get active Reservations with pagination support."""
        return self.db.get_active_reservations(db, pagination)

    def get_reservation_by_id(self, db: Session, reservation_id: int) -> DbReservation:
        """Get Reservation by ID."""
        return self.db.get_reservation_by_id(db, reservation_id)

    def reserve_product(self, db: Session, product_id: int, quantity: int) -> DbReservation:
        """Reserve Product by ID."""
        return self.db.reserve_product(db, product_id, quantity)

    def cancel_reservation(self, db: Session, reservation_id: int) -> Dict:
        """Cancel Reservation by ID."""
        return self.db.cancel_reservation(db, reservation_id)
