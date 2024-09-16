from typing import List, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..db.sqlalchemy_db.db_reservation import SqlalchemyReservationDatabase
from ..schemas.reservation_schemes import Reservation, QuantityRequest
from ..services.reservation_service import ReservationService
from ..request_utils import PaginationParams

router = APIRouter(
    prefix="/reservation",
    tags=["reservation"]
)

reservation_service = ReservationService(db=SqlalchemyReservationDatabase())


@router.get("/reservations", response_model=List[Reservation])
def get_reservations(db: Session = Depends(get_db), pagination: PaginationParams = Depends()) -> List[Reservation]:
    """Get all Reservations endpoint."""
    return reservation_service.get_reservations(db, pagination)


@router.get("/reservations/active", response_model=List[Reservation])
def get_active_reservations(db: Session = Depends(get_db), pagination: PaginationParams = Depends()) -> List[Reservation]:
    """Get active Reservations endpoint."""
    return reservation_service.get_active_reservations(db, pagination)


@router.get("/id/{reservation_id}", response_model=Reservation)
def get_reservation(reservation_id: int, db: Session = Depends(get_db)) -> List[Reservation]:
    """Get Reservation by ID endpoint."""
    return reservation_service.get_reservation_by_id(db, reservation_id)


@router.post("/reserve_product/{product_id}", response_model=Reservation)
def reserve_product(
    product_id: int,
    request: QuantityRequest,
    db: Session = Depends(get_db)
) -> Reservation:
    """Reserve Product by ID endpoint."""
    return reservation_service.reserve_product(db, product_id, request.quantity)


@router.delete("/id/{reservation_id}")
def cancel_reservation(reservation_id: int, db: Session = Depends(get_db)) -> Dict:
    """Cancel Reservation endpoint."""
    return reservation_service.cancel_reservation(db, reservation_id)
