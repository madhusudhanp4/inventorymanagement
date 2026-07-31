from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import Supplier
from app.schemas.supplier_schema import (SupplierCreate)

import time

from app.logging.logging_config import get_logger
from app.core.tracing import span

logger = get_logger()

router = APIRouter(
    prefix="/api/v1/suppliers",
    tags=["Suppliers"]
)


@router.post("/")
def create_supplier(
    request: SupplierCreate,
    db: Session = Depends(get_db)
):
    with span("http.request"):

        existing = (
            db.query(Supplier)
            .filter(
                Supplier.supplier_code ==
                request.supplier_code
            )
            .first()
        )

        if existing:
            return {
                "message": "Supplier already exists"
            }

        supplier = Supplier(
            name=request.name,
            supplier_code=request.supplier_code,
            contact_email=request.contact_email
        )

        db_start = time.time()

        db.add(supplier)
        db.commit()

        logger.info(
            "database_insert",
            poc_id="POC-07",
            phase=1,
            associate_id="Panuganti Madhusudan",
            operation="supplier_insert",
            duration_ms=int(
                (time.time() - db_start) * 1000
            ),
            status="success",
            error=None,
            request_id="db",
            extra={
                "table": "suppliers",
                "supplier_code": request.supplier_code
            }
        )

        db.refresh(supplier)

        return supplier




@router.get("/")
def get_suppliers(
    db: Session = Depends(get_db)
):
    with span("db.query"):

        db_start = time.time()

        result = db.query(
            Supplier
        ).all()

        logger.info(
            "database_query",
            poc_id="POC-07",
            phase=1,
            associate_id="Panuganti Madhusudan",
            operation="supplier_select",
            duration_ms=int(
                (time.time() - db_start) * 1000
            ),
            status="success",
            error=None,
            request_id="db",
            extra={
                "table": "suppliers"
            }
        )

        return result




@router.get("/{supplier_id}")
def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db)
):
    with span("db.query"):

        db_start = time.time()

        result = (
            db.query(Supplier)
            .filter(
                Supplier.id == supplier_id
            )
            .first()
        )

        logger.info(
            "database_query",
            poc_id="POC-07",
            phase=1,
            associate_id="Panuganti Madhusudan",
            operation="supplier_select_by_id",
            duration_ms=int(
                (time.time() - db_start) * 1000
            ),
            status="success",
            error=None,
            request_id="db",
            extra={
                "table": "suppliers",
                "supplier_id": supplier_id
            }
        )

        return result


@router.get("/{supplier_id}/catalog")
def supplier_catalog(
    supplier_id: int,
    db: Session = Depends(get_db)
):
    with span("db.query"):

        db_start = time.time()

        supplier = (
            db.query(Supplier)
            .filter(
                Supplier.id == supplier_id
            )
            .first()
        )

        logger.info(
            "database_query",
            poc_id="POC-07",
            phase=1,
            associate_id="Panuganti Madhusudan",
            operation="supplier_catalog",
            duration_ms=int(
                (time.time() - db_start) * 1000
            ),
            status="success",
            error=None,
            request_id="db",
            extra={
                "table": "suppliers",
                "supplier_id": supplier_id
            }
        )

        if not supplier:
            return []

        return supplier.products