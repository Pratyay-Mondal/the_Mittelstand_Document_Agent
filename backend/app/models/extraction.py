from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class ExtractionStatus(str, Enum):
    PENDING = "PENDING"
    REVIEWED = "REVIEWED"
    APPROVED = "APPROVED"

class ExtractionField(BaseModel):
    value: str | None = Field(description="The extracted value")
    confidence: float = Field(description="Confidence score between 0.0 and 1.0")
    source_page: Optional[int] = Field(description="The page number where the information was found", default=None)

class DocumentExtraction(BaseModel):
    invoice_number: Optional[ExtractionField] = Field(default=None, description="The invoice number")
    date: Optional[ExtractionField] = Field(default=None, description="The date of the invoice")
    total_amount: Optional[ExtractionField] = Field(default=None, description="The total amount of the invoice")
    vendor_name: Optional[ExtractionField] = Field(default=None, description="The name of the vendor/sender")
    vendor_address: Optional[ExtractionField] = Field(default=None, description="The address of the vendor")
    customer_name: Optional[ExtractionField] = Field(default=None, description="The name of the customer/recipient")
    tax_rate: Optional[ExtractionField] = Field(default=None, description="The tax rate applied")
    currency: Optional[ExtractionField] = Field(default=None, description="The currency of the amounts")

class DocumentState(BaseModel):
    doc_id: str
    filename: str
    page_count: int
    extraction: Optional[DocumentExtraction] = None
    extraction_status: ExtractionStatus = ExtractionStatus.PENDING
