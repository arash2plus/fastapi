from decimal import ROUND_HALF_UP, Decimal
from typing import List
from pydantic import BaseModel, Field, field_validator
import re


class Expense(BaseModel):
    id: int = Field(gt=0)
    description: str = Field(min_length=5, max_length=200)
    amount: float

    @field_validator("description")
    def validate_name(cls, value):
        pattern = r"^[a-zA-Z\s]+$"
        if not bool(re.match(pattern, value)):
            raise ValueError(
                "description cannot contain numbers,special characters or symbols"
            )
        return value

    @field_validator("amount")
    def amount_must_have_two_decimals(cls, value):
        decimal_value = Decimal(str(value)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        if decimal_value != Decimal(str(value)):
            raise ValueError("Amount must have exactly 2 decimal places")
        return float(decimal_value)


class ExpenseCreate(BaseModel):
    description: str = Field(min_length=5, max_length=200)
    amount: float

    @field_validator("description")
    def validate_name(cls, value):
        pattern = r"^[a-zA-Z\s]+$"
        if not bool(re.match(pattern, value)):
            raise ValueError(
                "description cannot contain numbers,special characters or symbols"
            )
        return value

    @field_validator("amount")
    def amount_must_have_two_decimals(cls, value):
        decimal_value = Decimal(str(value)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        if decimal_value != Decimal(str(value)):
            raise ValueError("Amount must have exactly 2 decimal places")
        return float(decimal_value)


class ExpenseUpdate(ExpenseCreate):
    pass


class ExpenseListResponse(Expense):
    id: int       
   
    class Config:
        orm_mode = True

class TotalAmountResponse(BaseModel):
    total_amount: float        
