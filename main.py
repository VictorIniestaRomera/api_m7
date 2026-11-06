from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    id: int
    nombre: str
    precio: float
    
# Datos en memoria (solo ejemplo)
items = [
    Item(id=1, nombre="Ejemplo 1", precio=2.5), 
    Item(id=2, nombre="Ejemplo 2", precio=1.9)
    ]

@app.get("/")
def helloWorld():
    return {"message": "Hello world!"}

@app.get("/items")
def listar_items():
    return items

@app.post("/items")
def crear_item(item: Item):
    items.append(item)

    return item

@app.put("/items/{id}")
def actualizar_item(id: int, item: Item):
    for i, it in enumerate(items):
        if it.id == id:
            items[i] = item

            return item
            
        raise HTTPException(status_code=404, detail="No encontrado")
        
@app.delete("/items/{id}")
def borrar_item(id: int):
    global items
    items = [it for it in items if it.id != id]

    return {"ok": True}