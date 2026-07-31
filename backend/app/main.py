from fastapi import FastAPI

from app.database.database import Base, engine

from app.routers.auth_router import router as auth_router
from app.routers.supplier_router import router as supplier_router
from app.routers.product_router import router as product_router
from app.routers.order_router import router as order_router
from app.routers.dashboard_router import router as dashboard_router

from app.logging.logging_config import get_logger

logger = get_logger()

# Create Database Tables
Base.metadata.create_all(bind=engine)

# Create FastAPI App
app = FastAPI(
    title="Inventory Management System"
)

# Register Routers
app.include_router(auth_router)
app.include_router(supplier_router)
app.include_router(product_router)
app.include_router(order_router)
app.include_router(dashboard_router)


@app.on_event("startup")
def startup_event():

    logger.info(
        "application_startup",
        poc_id="POC-07",
        phase=1,
        associate_id="Panuganti Madhusudan",
        operation="application_startup",
        duration_ms=0,
        status="success",
        error=None,
        request_id="system",
        extra={}
    )


@app.get("/")
def root():

    logger.info(
        "root_endpoint_called",
        poc_id="POC-07",
        phase=1,
        associate_id="Panuganti Madhusudan",
        operation="root_endpoint",
        duration_ms=0,
        status="success",
        error=None,
        request_id="system",
        extra={}
    )

    return {
        "message": "Inventory Management System API"
    }