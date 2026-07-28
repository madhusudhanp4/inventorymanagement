from pydantic import BaseModel
from typing import List, Optional


class POItemCreate(BaseModel):
    product_id: int
    quantity_ordered: int
    unit_cost: float


class PurchaseOrderCreate(BaseModel):
    supplier_id: int
    order_date: str
    expected_delivery: Optional[str] = None
    items: List[POItemCreate]