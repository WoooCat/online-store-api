from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
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


class DbDiscount(Base):
    __tablename__ = 'discounts'
    id = Column(Integer, primary_key=True, index=True)
    percentage = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    active = Column(Boolean, default=True)


class DbProductDiscount(Base):
    __tablename__ = 'product_discounts'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    discount_id = Column(Integer, ForeignKey('discounts.id'), nullable=False)
    product = relationship("DbProduct", backref="product_discounts")
    discount = relationship("DbDiscount", backref="product_discounts")


class DbReservation(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default='reserved')
    product = relationship("DbProduct", backref="reservations")

