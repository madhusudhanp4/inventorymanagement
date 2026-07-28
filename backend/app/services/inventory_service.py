from datetime import date

from sqlalchemy.orm import Session

from app.models.models import (
    CATEGORY_PREFIXES,
    Product,
    PurchaseOrder,
    StockLevel,
    StockAlert,
    StockMovement,
    MovementType,
    POStatus,
)


def generate_sku(category: str, db: Session) -> str:
    prefix = CATEGORY_PREFIXES.get(category, "GEN")

    count = (
        db.query(Product)
        .filter(Product.sku.like(f"SKU-{prefix}-%"))
        .count()
    )

    return f"SKU-{prefix}-{count + 1:04d}"


def generate_po_number(db: Session) -> str:
    year = date.today().year

    count = (
        db.query(PurchaseOrder)
        .filter(
            PurchaseOrder.po_number.like(
                f"PO-{year}-%"
            )
        )
        .count()
    )

    return f"PO-{year}-{count + 1:04d}"


def check_stock_alerts(
    product: Product,
    stock: StockLevel,
    db: Session,
):
    available = stock.quantity_available

    if available == 0:
        alert = StockAlert(
            product_id=product.id,
            alert_type="out_of_stock",
            message=f"SKU {product.sku} is OUT OF STOCK."
        )
        db.add(alert)

    elif available <= product.reorder_point:
        alert = StockAlert(
            product_id=product.id,
            alert_type="low_stock",
            message=(
                f"SKU {product.sku}: only "
                f"{available} units left."
            )
        )
        db.add(alert)


def receive_purchase_order(
    po_id: int,
    db: Session,
):
    po = (
        db.query(PurchaseOrder)
        .filter(
            PurchaseOrder.id == po_id
        )
        .first()
    )

    if not po:
        return None

    po.status = POStatus.received
    po.received_date = date.today()

    for item in po.items:

        qty = (
            item.quantity_received
            or item.quantity_ordered
        )

        item.quantity_received = qty

        stock = (
            db.query(StockLevel)
            .filter(
                StockLevel.product_id ==
                item.product_id
            )
            .first()
        )

        if stock:
            stock.quantity_on_hand += qty

        movement = StockMovement(
            product_id=item.product_id,
            movement_type=MovementType.receipt,
            quantity=qty,
            reference_number=po.po_number,
            notes=f"Received from {po.po_number}",
        )

        db.add(movement)

        (
            db.query(StockAlert)
            .filter(
                StockAlert.product_id ==
                item.product_id,
                StockAlert.is_resolved == False,
            )
            .update(
                {"is_resolved": True}
            )
        )

    db.commit()

    return po