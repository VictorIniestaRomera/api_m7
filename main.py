import json;
from pathlib import Path;

from fastapi import FastAPI, HTTPException;
from pydantic import BaseModel;

app = FastAPI();
STORAGE_PATH = Path(__file__).with_name("storage.json");

class Fruit(BaseModel):
    id: int;
    name: str;
    price: float;
    quantity: int;

def loadItems() -> list[Fruit]:
    contents = STORAGE_PATH.read_text(encoding="utf-8");

    if not contents.strip():
        return [];
    
    return [Fruit.model_validate(item) for item in json.loads(contents)];

def saveItem(updated_items: list[Fruit]) -> None:
    STORAGE_PATH.write_text(json.dumps([item.model_dump() for item in updated_items], indent=2), encoding="utf-8");

items = loadItems();

@app.get("/")
def introduction():
    return {"message": "Welcome to my fruit shop!"};

@app.get("/fruits")
def listItems():
    return items;

@app.post("/fruits")
def createItem(item: Fruit):
    if item.id == 0:
        item.id = len(items);
    
    updated_items = [*items, item];

    saveItem(updated_items);

    items.append(item);

    return item;

@app.put("/fruits/{id}")
def updateItem(id: int, item: Fruit):
    for i, it in enumerate(items):
        if it.id == id:
            updated_items = [*items];
            updated_items[i] = item;

            saveItem(updated_items);

            items[i] = item;

            return item;
            
        raise HTTPException(status_code=404, detail="No encontrado");
        
@app.delete("/fruits/{id}")
def deleteItem(id: int):
    updated_items = [it for it in items if it.id != id];

    saveItem(updated_items);

    items[:] = updated_items;

    return {"ok": True};