from pydantic import BaseModel, Field


"""RESERVATION SCHEMAS"""


class ReservationBase(BaseModel):
    product_id: int
    quantity: int


class ReservationCreate(ReservationBase):
    pass


class Reservation(ReservationBase):
    id: int
    status: str

    class Config:
        from_attributes = True


class QuantityRequest(BaseModel):
    quantity: int = Field(..., gt=0)
