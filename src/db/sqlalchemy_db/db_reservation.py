from typing import Dict, List

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ...enums import FilterField, ReservationStatus
from ...request_utils import PaginationParams, apply_pagination, get_object_or_404
from ..abstract.db_abstract_reservation import AbstractReservationDatabase
from ..models import DbProduct, DbReservation


class SqlalchemyReservationDatabase(AbstractReservationDatabase):
    """SQLAlchemy implementation of the AbstractReservationDatabase for managing Reservations in the database."""

    def get_reservations(self, db: Session, pagination: PaginationParams) -> List[DbReservation]:
        """Get all Reservations from the database."""
        db_reservations = db.query(DbReservation)
        return apply_pagination(db_reservations, pagination)

    def get_active_reservations(self, db: Session, pagination: PaginationParams) -> List[DbReservation]:
        """Get active Reservations from the database."""
        db_reservations = db.query(DbReservation).filter(DbReservation.status == ReservationStatus.RESERVED.value)
        return apply_pagination(db_reservations, pagination)

    def get_reservation_by_id(self, db: Session, reservation_id: int) -> DbReservation:
        """Get Reservation by ID from the database."""
        return get_object_or_404(DbReservation, FilterField.ID, reservation_id, db)

    def reserve_product(self, db: Session, product_id: int, quantity: int) -> DbReservation:
        """Reserve Product by ID in the database."""
        db_product = get_object_or_404(DbProduct, FilterField.ID, product_id, db)
        if db_product.stock < quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock, {db_product.stock} units remain.")
        db_product.stock -= quantity
        db_product.reserved_stock += quantity

        db_reservation = DbReservation(product_id=product_id, quantity=quantity)
        db.add(db_reservation)
        db.commit()
        db.refresh(db_reservation)
        return db_reservation

    def cancel_reservation(self, db: Session, reservation_id: int) -> Dict:
        """Cancel Reservation by ID in the database."""
        db_reservation = get_object_or_404(DbReservation, FilterField.ID, reservation_id, db)
        if db_reservation.status != ReservationStatus.RESERVED.value:
            raise HTTPException(status_code=404, detail=f"Reservation with '{reservation_id}' not found or 'canceled'")

        db_product = db.query(DbProduct).filter(DbProduct.id == db_reservation.product_id).first()
        db_product.stock += db_reservation.quantity
        db_product.reserved_stock -= db_reservation.quantity
        db_reservation.status = ReservationStatus.CANCELLED.value
        db.commit()
        return {"message": f"Reservation with 'id': '{db_reservation.id}' cancelled successfully."}
