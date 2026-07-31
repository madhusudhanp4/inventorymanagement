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

import time

from app.logging.logging_config import get_logger

logger = get_logger()


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

        db_start = time.time()

        db.add(po)
        db.commit()

        logger.info(
            "database_insert",
            poc_id="POC-07",
            phase=1,
            associate_id="Panuganti Madhusudan",
            operation="purchase_order_insert",
            duration_ms=int(
                (time.time() - db_start) * 1000
            ),
            status="success",
            error=None,
            request_id="db",
            extra={
                "table": "purchase_orders"
            }
        )

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

        db_start = time.time()

        db.commit()

        logger.info(
            "database_insert",
            poc_id="POC-07",
            phase=1,
            associate_id="Panuganti Madhusudan",
            operation="purchase_order_item_insert",
            duration_ms=int(
                (time.time() - db_start) * 1000
            ),
            status="success",
            error=None,
            request_id="db",
            extra={
                "table": "po_items",
                "po_id": po.id
            }
        )

        db.refresh(po)

        return po




@router.get("/")
def get_orders(
    db: Session = Depends(get_db)
):
    with span("db.query"):

        db_start = time.time()

        result = db.query(
            PurchaseOrder
        ).all()

        logger.info(
            "database_query",
            poc_id="POC-07",
            phase=1,
            associate_id="Panuganti Madhusudan",
            operation="purchase_order_select",
            duration_ms=int(
                (time.time() - db_start) * 1000
            ),
            status="success",
            error=None,
            request_id="db",
            extra={
                "table": "purchase_orders"
            }
        )

        return result


@router.get("/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    with span("db.query"):

        db_start = time.time()

        result = (
            db.query(PurchaseOrder)
            .filter(
                PurchaseOrder.id == order_id
            )
            .first()
        )

        logger.info(
            "database_query",
            poc_id="POC-07",
            phase=1,
            associate_id="Panuganti Madhusudan",
            operation="purchase_order_select_by_id",
            duration_ms=int(
                (time.time() - db_start) * 1000
            ),
            status="success",
            error=None,
            request_id="db",
            extra={
                "table": "purchase_orders",
                "order_id": order_id
            }
        )

        return result



@router.patch("/{order_id}/receive")
def receive_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    with span("http.request"):

        db_start = time.time()

        po = receive_purchase_order(
            order_id,
            db
        )

        logger.info(
            "database_update",
            poc_id="POC-07",
            phase=1,
            associate_id="Panuganti Madhusudan",
            operation="purchase_order_receive",
            duration_ms=int(
                (time.time() - db_start) * 1000
            ),
            status="success" if po else "failure",
            error=None if po else "order_not_found",
            request_id="db",
            extra={
                "table": "purchase_orders",
                "order_id": order_id
            }
        )

        if not po:
            return {
                "message": "Order not found"
            }

        return {
            "message": "Purchase Order Received"
        }