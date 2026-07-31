from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import Supplier
from app.schemas.supplier_schema import (
    SupplierCreate
)

router = APIRouter(
    prefix="/api/v1/suppliers",
    tags=["Suppliers"]
)


@router.post("/")
def create_supplier(
    request: SupplierCreate,
    db: Session = Depends(get_db)
):
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

    db.add(supplier)
    db.commit()
    db.refresh(supplier)

    return supplier


@router.get("/")
def get_suppliers(
    db: Session = Depends(get_db)
):
    return db.query(Supplier).all()


@router.get("/{supplier_id}")
def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db)
):
    return (
        db.query(Supplier)
        .filter(Supplier.id == supplier_id)
        .first()
    )


@router.get("/{supplier_id}/catalog")
def supplier_catalog(
    supplier_id: int,
    db: Session = Depends(get_db)
):
    supplier = (
        db.query(Supplier)
        .filter(Supplier.id == supplier_id)
        .first()
    )

    if not supplier:
        return []

    return supplier.products