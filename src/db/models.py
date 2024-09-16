from sqlalchemy import Column, Integer, String, ForeignKey, Float
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


class DbProduct(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    reserved_stock = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("DbCategory", backref="products")

    @property
    def category_name(self):
        return self.category.name if self.category else None
