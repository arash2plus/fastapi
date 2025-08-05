import uuid

from fastapi import FastAPI,HTTPException

from typing import Dict


app = FastAPI()

cost_items_db: Dict[str, Dict] = {}
cost_id = 0


@app.post("/create")
async def create_item(description:str, cost:float):
     cost_id = str(uuid.uuid4())
     cost_items = {
          'id': cost_id,
          'description' : description,
          'cost': float(cost)
     }
     

     cost_items_db[cost_id] = cost_items
     return cost_items


@app.get("/costs")
async def get_all_costs():
     return list(cost_items_db.values())


@app.get("/cost/{cost_id}")
async def get_cost_item(cost_id: str):
     if cost_id not in cost_items_db:
          raise HTTPException(status_code=404,detail="Cost item not found!")
     return cost_items_db[cost_id]

@app.put("/cost/{cost_id}")
async def update_cost_item(cost_id: str, description: str, cost: float):
     if cost_id not in cost_items_db:
          raise HTTPException(status_code=404,detail="Cost item not found!")
     cost_items_db[cost_id][description] = description
     cost_items_db[cost_id][cost] = cost
     return cost_items_db[cost_id]


@app.delete("/cost/{cost_id}")
async def delete_cost_item(cost_id: str):
     if cost_id not in cost_items_db:
          raise HTTPException(status_code=404,detail="Cost item not found!")
     deleted_item = cost_items_db.pop(cost_id)     
     return {"message": "Cost deleted", "deleted_item": deleted_item}


@app.get('/cost/total/')
async def get_total_items():
     total_costs = 0
     for item in cost_items_db.values():
          total_costs += item['cost']
    #  total_costs = sum(item['cost'] for item in cost_items_db.values())     
     return {"Total Costs": total_costs }  









                     





      
          

