from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.models import (
    Product,
    StockLevel,
    Category
)
from app.schemas.product_schema import (
    ProductCreate
)
from app.services.inventory_service import (
    generate_sku
)

from app.models.models import (
    StockMovement,
    StockAlert
)

from app.schemas.stock_schema import (
    StockMovementRequest
)

from app.services.inventory_service import (
    check_stock_alerts
)



router = APIRouter(
    prefix="/api/v1/products",
    tags=["Products"]
)


@router.post("/", status_code=201)
def create_product(
    request: ProductCreate,
    db: Session = Depends(get_db)
):
    sku = generate_sku(
        request.category,
        db
    )

    product = Product(
        sku=sku,
        name=request.name,
        category=Category(request.category),
        unit_price=request.unit_price,
        cost_price=request.cost_price,
        unit_of_measure=request.unit_of_measure,
        reorder_point=request.reorder_point,
        reorder_quantity=request.reorder_quantity,
        supplier_id=request.supplier_id
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    stock = StockLevel(
        product_id=product.id,
        quantity_on_hand=0,
        quantity_reserved=0
    )

    db.add(stock)
    db.commit()

    return product


@router.get("/")
def get_products(
    category: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    if category:
        query = query.filter(
            Product.category == category
        )

    return query.all()


@router.get("/{product_id}")
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    return (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )


@router.patch("/{product_id}/stock")
def update_stock(
    product_id: int,
    request: StockMovementRequest,
    db: Session = Depends(get_db)
):
    product = (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )

    if not product:
        return {
            "message": "Product not found"
        }

    stock = (
        db.query(StockLevel)
        .filter(
            StockLevel.product_id == product_id
        )
        .first()
    )

    if not stock:
        return {
            "message": "Stock record not found"
        }

    stock.quantity_on_hand += request.quantity

    movement = StockMovement(
        product_id=product_id,
        movement_type=request.movement_type,
        quantity=request.quantity,
        reference_number=request.reference_number,
        notes=request.notes
    )

    db.add(movement)

    check_stock_alerts(
        product,
        stock,
        db
    )

    db.commit()

    return {
        "message": "Stock Updated Successfully",
        "quantity_on_hand": stock.quantity_on_hand
    }