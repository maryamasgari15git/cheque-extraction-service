from typing import Optional
from pydantic import BaseModel


class ExtractedField(BaseModel):
    value: Optional[str] = None
    confidence: float = 0


class ChequeData(BaseModel):
    sayad_id: ExtractedField
    cheque_number: ExtractedField
    amount_digits: ExtractedField
    amount_words: ExtractedField
    due_date: ExtractedField
    payee: ExtractedField
    description: ExtractedField
    bank_name: ExtractedField
    account_number: ExtractedField
    branch_code: ExtractedField


class ChequeExtractionResponse(BaseModel):
    success: bool
    data: Optional[ChequeData] = None
    processing_time_ms: Optional[int] = None