from typing import List, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db.sqlalchemy_db.db_product import SqlalchemyProductDatabase
from ..schemas.product_schemes import ProductCreate, ProductUpdate, Product, ProductPriceUpdate
from ..db.database import get_db
from ..services.product_service import ProductService
from ..request_utils import PaginationParams

router = APIRouter(
    prefix="/product",
    tags=["product"],
)

product_service = ProductService(db=SqlalchemyProductDatabase())


@router.get("/products", response_model=List[Product])
def get_products(db: Session = Depends(get_db), pagination: PaginationParams = Depends()) -> List[Product]:
    """Get all Products endpoint."""
    return product_service.get_products(db, pagination)


@router.post("/create", response_model=Product)
def create_product(request: ProductCreate, db: Session = Depends(get_db)) -> Product:
    """Create new Product endpoint."""
    return product_service.create_product(db, request)


@router.get("/id/{product_id}", response_model=Product)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)) -> Product:
    """Get Product by ID endpoint."""
    return product_service.get_product_by_id(db, product_id)


@router.get("/name/{name}", response_model=Product)
def get_product_by_name(name: str, db: Session = Depends(get_db)) -> Product:
    """Get Product by Name endpoint"""
    return product_service.get_product_by_name(db, name)


@router.get("/category/{category_id}", response_model=List[Product])
def get_products_by_category(
        category_id: int,
        db: Session = Depends(get_db),
        pagination: PaginationParams = Depends(),
) -> List[Product]:
    return product_service.get_products_by_category(db, category_id, pagination)


@router.patch("/update/{id}", response_model=Product)
def update_product(request: ProductUpdate, product_id: int, db: Session = Depends(get_db)) -> Product:
    """Update Product by ID endpoint"""
    return product_service.update_product(db, product_id, request)


@router.patch("/{product_id}/price", response_model=Product)
def update_product_price(product_id: int, request: ProductPriceUpdate, db: Session = Depends(get_db)) -> Product:
    """Update price of Product by ID."""
    return product_service.update_product_price(db, product_id, request.price)


@router.delete("/delete/{product_id}", response_model=Dict)
def remove_product(product_id: int, db: Session = Depends(get_db)) -> Dict:
    """Remove Product by ID endpoint."""
    return product_service.remove_product(db, product_id)
