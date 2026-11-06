from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Fruit(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    
# Datos en memoria (solo ejemplo)
items = [
    Fruit(id=1, name="Apple", price=2.5, quantity=30), 
    Fruit(id=2, name="Pear", price=1.9, quantity=20)
    ]

@app.get("/")
def introduction():
    return {"message": "Welcome to my fruit shop!"}

@app.get("/fruits")
def listItems():
    return items

@app.post("/fruits")
def createItem(item: Fruit):
    items.append(item)

    return item

@app.put("/fruits/{id}")
def updateItem(id: int, item: Fruit):
    for i, it in enumerate(items):
        if it.id == id:
            items[i] = item

            return item
            
        raise HTTPException(status_code=404, detail="No encontrado")
        
@app.delete("/fruits/{id}")
def deleteItem(id: int):
    global items
    items = [it for it in items if it.id != id]

    return {"ok": True}