from fastapi import FastAPI
from src.db import models
from src.db.database import engine
from src.routers import category


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


models.Base.metadata.create_all(engine)
