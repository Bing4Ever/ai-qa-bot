from pydantic import BaseModel

class Invoice(BaseModel):
    invoice_number: str
    date: str
    issuer: str
    subtotal: str
    tax_rate: str
    total_amount: str
    category: str