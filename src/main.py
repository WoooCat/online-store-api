from fastapi import FastAPI
from src.db import models
from src.db.database import engine
from src.routers import category, product


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


models.Base.metadata.create_all(engine)
