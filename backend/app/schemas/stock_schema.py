from pydantic import BaseModel
from typing import Optional


class StockMovementRequest(BaseModel):
    movement_type: str
    quantity: int
    reference_number: Optional[str] = None
    notes: Optional[str] = None