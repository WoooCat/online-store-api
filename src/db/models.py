from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class DbCategory(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)
    parent = relationship("DbCategory", remote_side=[id], backref="children")


class DbCategoryRelation(Base):
    __tablename__ = 'category_relations'
    id = Column(Integer, primary_key=True, index=True)
    ancestor_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    descendant_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    depth = Column(Integer, nullable=False)
