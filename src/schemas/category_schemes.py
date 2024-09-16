from typing import Optional, List
from pydantic import BaseModel


"""CATEGORY SCHEMES"""


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    parent_id: Optional[int] = None


class CategoryUpdate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    children: List['Category'] = []

    class Config:
        from_attributes = True
