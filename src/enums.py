from enum import Enum


class FilterField(str, Enum):
    ID = "id"
    NAME = "name"
    CATEGORY_ID = "category_id"
