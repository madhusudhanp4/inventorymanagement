from datetime import datetime

from app.core.tracing import span

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import (
    PurchaseOrder,
    POItem,
    Product
)
from app.schemas.order_schema import (
    PurchaseOrderCreate
)
from app.services.inventory_service import (
    generate_po_number,
    receive_purchase_order
)

router = APIRouter(
    prefix="/api/v1/orders",
    tags=["Orders"]
)


@router.post("/", status_code=201)
def create_order(
    request: PurchaseOrderCreate,
    db: Session = Depends(get_db)
):
    with span("http.request"):

        po = PurchaseOrder(
            po_number=generate_po_number(db),
            supplier_id=request.supplier_id,
            order_date=datetime.strptime(
                request.order_date,
                "%Y-%m-%d"
            ).date(),
            status="draft"
        )

        db.add(po)
        db.commit()
        db.refresh(po)

        total_amount = 0

        for item in request.items:

            total_amount += (
                item.quantity_ordered *
                item.unit_cost
            )

            po_item = POItem(
                po_id=po.id,
                product_id=item.product_id,
                quantity_ordered=item.quantity_ordered,
                unit_cost=item.unit_cost
            )

            db.add(po_item)

        po.total_amount = total_amount

        db.commit()
        db.refresh(po)

        return po

        


@router.get("/")
def get_orders(
    db: Session = Depends(get_db)
):
    with span("db.query"):

        return db.query(
            PurchaseOrder
        ).all()



@router.get("/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    with span("db.query"):

        return (
            db.query(PurchaseOrder)
            .filter(
                PurchaseOrder.id == order_id
            )
            .first()
        )



@router.patch("/{order_id}/receive")
def receive_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    with span("http.request"):

        po = receive_purchase_order(
            order_id,
            db
        )

        if not po:
            return {
                "message": "Order not found"
            }

        return {
            "message": "Purchase Order Received"
        }