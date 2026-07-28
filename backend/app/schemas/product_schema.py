from pydantic import BaseModel
from typing import Optional


class ProductCreate(BaseModel):
    name: str
    category: str
    unit_price: float
    cost_price: float
    unit_of_measure: str = "pieces"
    reorder_point: int = 10
    reorder_quantity: int = 50
    supplier_id: Optional[int] = None


class ProductResponse(BaseModel):
    id: int
    sku: str
    name: str
    category: str
    unit_price: float
    cost_price: float
    unit_of_measure: str
    reorder_point: int
    reorder_quantity: int

    class Config:
        from_attributes = True