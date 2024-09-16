from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.db import models
from src.db.database import engine
from src.routers import category, discount, product, reservation, sale

app = FastAPI(
    title="Online Store",
    description="Test Online Store",
    version="1.0.0"
)


app.include_router(category.router)
app.include_router(product.router)
app.include_router(discount.router)
app.include_router(reservation.router)
app.include_router(sale.router)


models.Base.metadata.create_all(engine)


@app.get("/status", tags=["Test"])
async def status_endpoint():
    """Endpoint to return status message."""
    return {"status": "Online"}


@app.get("/", include_in_schema=False)
async def root_redirect():
    """Redirect to the Swagger UI documentation."""
    return RedirectResponse(url="/docs")


origins = [
  'http://localhost:8000',
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
