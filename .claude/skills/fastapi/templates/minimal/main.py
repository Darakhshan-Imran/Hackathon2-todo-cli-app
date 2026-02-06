"""
FastAPI Minimal Template
A single-file FastAPI application for learning and prototyping.

Setup: uv sync
Run with: uv run fastapi dev main.py
Docs at: http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(
    title="My API",
    description="A minimal FastAPI application",
    version="1.0.0"
)

# ============== Models ==============

class ItemBase(BaseModel):
    """Base model for Item"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    is_available: bool = True


class ItemCreate(ItemBase):
    """Model for creating an item"""
    pass


class ItemResponse(ItemBase):
    """Model for item response"""
    id: int
    created_at: datetime


# ============== In-Memory Database ==============

items_db: dict[int, dict] = {}
item_counter = 0


# ============== Endpoints ==============

@app.get("/")
def root():
    """Welcome endpoint"""
    return {"message": "Welcome to My API!", "docs": "/docs"}


@app.get("/items", response_model=List[ItemResponse])
def list_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return"),
    available_only: bool = Query(False, description="Filter available items only")
):
    """List all items with pagination"""
    items = list(items_db.values())

    if available_only:
        items = [item for item in items if item["is_available"]]

    return items[skip : skip + limit]


@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    """Get a single item by ID"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate):
    """Create a new item"""
    global item_counter
    item_counter += 1

    new_item = {
        "id": item_counter,
        **item.model_dump(),
        "created_at": datetime.now()
    }
    items_db[item_counter] = new_item
    return new_item


@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemCreate):
    """Update an existing item"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    items_db[item_id].update(item.model_dump())
    return items_db[item_id]


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    """Delete an item"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    del items_db[item_id]
    return None


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "items_count": len(items_db)}
