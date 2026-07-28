from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import (
    Product,
    StockLevel,
    PurchaseOrder,
    POStatus
)

router = APIRouter(
    prefix="/api/v1",
    tags=["Dashboard"]
)


@router.get("/stock/low-alerts")
def get_low_stock_alerts(
    db: Session = Depends(get_db)
):
    results = []

    products = db.query(Product).all()

    for product in products:

        stock = (
            db.query(StockLevel)
            .filter(
                StockLevel.product_id == product.id
            )
            .first()
        )

        if not stock:
            continue

        if stock.quantity_available <= product.reorder_point:

            results.append({
                "id": product.id,
                "sku": product.sku,
                "name": product.name,
                "quantity_available":
                    stock.quantity_available,
                "reorder_point":
                    product.reorder_point
            })

    return results


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db)
):
    products = db.query(Product).all()

    total_products = len(products)

    low_stock_count = 0
    out_of_stock_count = 0
    total_stock_value = 0

    for product in products:

        stock = (
            db.query(StockLevel)
            .filter(
                StockLevel.product_id ==
                product.id
            )
            .first()
        )

        if not stock:
            continue

        if stock.quantity_available == 0:
            out_of_stock_count += 1

        if stock.quantity_available <= product.reorder_point:
            low_stock_count += 1

        total_stock_value += (
            stock.quantity_on_hand *
            product.cost_price
        )

    open_po_count = (
        db.query(PurchaseOrder)
        .filter(
            PurchaseOrder.status !=
            POStatus.received
        )
        .count()
    )

    return {
        "total_products": total_products,
        "low_stock_count": low_stock_count,
        "out_of_stock_count": out_of_stock_count,
        "open_po_count": open_po_count,
        "total_stock_value": total_stock_value
    }