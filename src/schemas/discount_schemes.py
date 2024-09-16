from typing import Optional

from pydantic import BaseModel, Field

"""DISCOUNT SCHEMES"""


class DiscountBase(BaseModel):
    percentage: float = Field(
        ...,
        ge=0,
        le=100,
        description="Discount percentage must be between 0 and 100.",
    )
    description: Optional[str] = None


class DiscountCreate(DiscountBase):
    pass


class DiscountUpdate(BaseModel):
    percentage: Optional[float] = None
    description: Optional[str] = None
    active: Optional[bool] = None


class Discount(DiscountBase):
    id: int
    active: bool

    class Config:
        from_attributes = True


class ProductDiscountBase(BaseModel):
    discount_id: int


class ProductDiscountCreate(ProductDiscountBase):
    pass


class ProductDiscount(ProductDiscountBase):
    id: int
    product_id: int

    class Config:
        from_attributes = True
