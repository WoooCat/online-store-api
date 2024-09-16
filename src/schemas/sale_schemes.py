from pydantic import BaseModel

"""RESERVATION SCHEMES"""


class SaleBase(BaseModel):
    product_id: int
    quantity: int
    sale_price: float

    class Config:
        from_attributes = True


class Sale(SaleBase):
    id: int
