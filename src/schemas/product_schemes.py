from pydantic import BaseModel, Field, field_validator

"""PRODUCT SCHEMES"""


class ProductBase(BaseModel):
    name: str
    stock: int
    category_id: int


class ProductCreate(ProductBase):
    price: float


class ProductUpdate(ProductBase):
    pass


class ProductPriceUpdate(BaseModel):
    price: float = Field(
        ...,
        ge=0,
        description="The price of the product must be greater or equal 0."
    )

    @field_validator('price')
    def price_must_be_non_negative(cls, value):
        if value < 0:
            raise ValueError('Price must be greater or equal to 0.')
        return value


class Product(ProductBase):
    id: int
    reserved_stock: int
    price: float
    category_name: str

    class Config:
        from_attributes = True
