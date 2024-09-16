from fastapi import FastAPI

from src.db import models
from src.db.database import engine
from src.routers import category, discount, product, reservation, sale

app = FastAPI(
    title="Online Store",
    description="Test Online Store",
    version="1.0.0"
)


@app.get("/status", tags=["Test"])
async def status_endpoint():
    """Endpoint to return status message."""
    return {"status": "Online"}


app.include_router(category.router)
app.include_router(product.router)
app.include_router(discount.router)
app.include_router(reservation.router)
app.include_router(sale.router)


models.Base.metadata.create_all(engine)
