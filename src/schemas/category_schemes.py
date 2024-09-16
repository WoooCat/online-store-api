from typing import List, Optional

from pydantic import BaseModel

"""CATEGORY SCHEMES"""


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    parent_id: Optional[int] = None

    def dict(self, *args, **kwargs) -> dict:
        data = super().dict(*args, **kwargs)
        if data.get('parent_id') == 0:
            data.pop('parent_id')
        return data


class CategoryUpdate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    children: List['Category'] = []

    class Config:
        from_attributes = True
