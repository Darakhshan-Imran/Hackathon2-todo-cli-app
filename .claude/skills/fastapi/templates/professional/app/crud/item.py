"""Item CRUD operations."""

from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


def get_item(db: Session, item_id: int) -> Optional[Item]:
    """Get item by ID."""
    return db.query(Item).filter(Item.id == item_id).first()


def get_items(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    available_only: bool = False
) -> List[Item]:
    """Get all items with pagination."""
    query = db.query(Item)
    if available_only:
        query = query.filter(Item.is_available == True)
    return query.offset(skip).limit(limit).all()


def get_user_items(db: Session, user_id: int) -> List[Item]:
    """Get items for a specific user."""
    return db.query(Item).filter(Item.owner_id == user_id).all()


def create_item(db: Session, item: ItemCreate, owner_id: Optional[int] = None) -> Item:
    """Create a new item."""
    db_item = Item(**item.model_dump(), owner_id=owner_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item_update: ItemUpdate) -> Optional[Item]:
    """Update an item."""
    db_item = get_item(db, item_id)
    if not db_item:
        return None

    update_data = item_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item


def delete_item(db: Session, item_id: int) -> bool:
    """Delete an item."""
    db_item = get_item(db, item_id)
    if not db_item:
        return False

    db.delete(db_item)
    db.commit()
    return True
