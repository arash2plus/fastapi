from decimal import ROUND_HALF_UP, Decimal
import re
from typing import List
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator



app = FastAPI()

expenses_db = [
    {"id": 1, "description": "mac book", "amount": 2500},
    {"id": 2, "description": "tablet", "amount": 3000},
    {"id": 3, "description": "tablet", "amount": 1450},
]


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


class ExpenseListResponse(BaseModel):
    expenses : List[Expense]


#####
# create api
@app.post("/create", status_code=status.HTTP_201_CREATED)
async def create_expense(expense_item: ExpenseCreate):
    last_id = expenses_db[-1]["id"] if expenses_db else 0
    last_id = int(last_id + 1)
    new_expense = {
        "id": last_id,
        "description": expense_item.description,
        "amount": expense_item.amount,
    }
    expenses_db.append(new_expense)
    return new_expense


#####
# List api
@app.get(
    "/cost-list", response_model=ExpenseListResponse, status_code=status.HTTP_200_OK
)
async def cost_list():
    return {"expenses": expenses_db}


#####
# Update api
@app.put(
    "/cost/{cost_id}",
    response_model=ExpenseUpdate,
    status_code=status.HTTP_200_OK
)
async def cost_update(cost_id: int, expense_item: ExpenseUpdate):
    for item in expenses_db:
        if item["id"] == cost_id:
            item["description"] = expense_item.description
            item["amount"] = expense_item.amount
            return item

    raise HTTPException(status_code=404, detail="id not found")


#####
# Delete api
@app.delete("/cost/{cost_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cost_to_delete(cost_id: int):
    for i in range(len(expenses_db)):
        if expenses_db[i]["id"] == cost_id:
            deleted_item = expenses_db.pop(i)
            return {"message": "Item deleted", "deleted_item": deleted_item}

    raise HTTPException(status_code=404, detail="id not found")


#####
# Sum api
@app.get("/all-items-cost", status_code=status.HTTP_200_OK)
async def all_items_cost():
    total = sum(item["amount"] for item in expenses_db)
    return {"total_cost": total}
