from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from schemas import ExpenseCreate, ExpenseUpdate, ExpenseListResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import ExpenseModel


app = FastAPI(title="Expense Tracker API")


@app.post("/create", status_code=status.HTTP_201_CREATED)
async def create_expense(request: ExpenseCreate, db: Session = Depends(get_db)):
    new_expense = ExpenseModel(
        description = request.description,
        amount = request.amount
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return  new_expense

@app.get("/all", status_code=status.HTTP_200_OK,response_model= List[ExpenseListResponse])
async def get_all_expenses(db: Session = Depends(get_db)):
    all_expenses = db.query(ExpenseModel).all()
    return all_expenses

@app.get("/expenses/{expense_id}", status_code=status.HTTP_200_OK)
async def get_expense(expense_id: int,db: Session = Depends(get_db)):
    expense_item = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    if not expense_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return expense_item

@app.put("/expenses/{expense_id}", response_model= ExpenseUpdate)
async def update_expense(expense_id: int,request: ExpenseUpdate,db: Session = Depends(get_db)):
    expense_item = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    if not expense_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    expense_item.description = request.description
    expense_item.amount = request.amount
    db.commit()
    db.refresh(expense_item)
    return expense_item

@app.delete("/expenses/{expense_id}")
async def delete_expense(expense_id: int,db: Session = Depends(get_db)):
    expense_item = db.query(ExpenseModel).filter(ExpenseModel.id == expense_id).first()
    if not expense_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(expense_item)
    db.commit()
    return "delete successfully..."

@app.get("/total", status_code=status.HTTP_200_OK)
async def get_total_expenses(db: Session = Depends(get_db)):
    total = db.query(func.sum(ExpenseModel.amount)).scalar() or 0.0
    return {"total": total}







   









