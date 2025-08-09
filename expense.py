from fastapi import FastAPI,HTTPException

app =  FastAPI()


expenses_db = [
    {"id": 1, "description": "mac book", "amount": 2500},
    {"id": 2, "description": "tablet", "amount": 3000},
    {"id": 3, "description": "tablet", "amount": 1450}
]


@app.post("/create-item")
async def create_item(desc: str, amount:float):
    last_id = expenses_db[-1]["id"] 
    last_id = int(last_id + 1)
    new_expense = {
        "id": last_id,
        "description": desc,
        "amount" : amount
    }
    expenses_db.append(new_expense)
    return new_expense

@app.get("/cost-list")
async def cost_list():
    return expenses_db


@app.put("/cost/{cost_id}")
async def cost_update(cost_id: int,desc: str, amount:float):
    for item in expenses_db:
        if item["id"] == cost_id:
           item["description"] = desc
           item["amount"] = amount
           return item 
            
    raise HTTPException(status_code=404,detail="id not found")

  
@app.delete("/cost/{cost_id}")
async def cost_to_delete(cost_id: int):
    for i in range(len(expenses_db)):
        if expenses_db[i]["id"] == cost_id:
            deleted_item = expenses_db.pop(i)
            return {"message": "Item deleted", "deleted_item": deleted_item}
    
    raise HTTPException(status_code=404, detail="id not found")


@app.get("/all-items-cost")
async def all_items_cost():
    total = sum(item["amount"] for item in expenses_db)
    return {"total_cost": total}

    



      
    

    
    

    



