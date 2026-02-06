"""Items router."""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.crud import item as crud_item
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.core.security import get_current_active_user

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=List[ItemResponse])
def list_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    available_only: bool = Query(False),
    db: Session = Depends(get_db)
):
    """List all items (public)."""
    return crud_item.get_items(db, skip=skip, limit=limit, available_only=available_only)


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Get an item by ID (public)."""
    item = crud_item.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(
    item: ItemCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Create an item (authenticated)."""
    return crud_item.create_item(db, item, owner_id=current_user.id)


@router.patch("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    item_update: ItemUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Update an item (authenticated, owner only)."""
    db_item = crud_item.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    if db_item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this item")

    return crud_item.update_item(db, item_id, item_update)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Delete an item (authenticated, owner only)."""
    db_item = crud_item.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    if db_item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this item")

    crud_item.delete_item(db, item_id)
    return None


@router.get("/my/items", response_model=List[ItemResponse])
def list_my_items(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """List current user's items (authenticated)."""
    return crud_item.get_user_items(db, current_user.id)
