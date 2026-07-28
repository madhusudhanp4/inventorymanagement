from fastapi import FastAPI

from app.database.database import Base, engine
from app.models.models import *
from app.routers.auth_router import router as auth_router
from app.routers.supplier_router import router as supplier_router
from app.routers.product_router import router as product_router
from app.routers.order_router import router as order_router
from app.routers.dashboard_router import (router as dashboard_router)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventory Management System"
)

app.include_router(auth_router)
app.include_router(supplier_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(dashboard_router)


@app.get("/")
def root():
    return {
        "message": "Inventory Management System API"
    }