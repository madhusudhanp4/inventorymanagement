from pydantic import BaseModel


class SupplierCreate(BaseModel):
    name: str
    supplier_code: str
    contact_email: str


class SupplierResponse(BaseModel):
    id: int
    name: str
    supplier_code: str
    contact_email: str

    class Config:
        from_attributes = True