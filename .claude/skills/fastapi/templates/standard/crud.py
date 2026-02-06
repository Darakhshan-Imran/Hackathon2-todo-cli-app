"""CRUD operations for database models."""

from sqlalchemy.orm import Session
from typing import Optional, List
from passlib.context import CryptContext

from models import User, Item
from schemas import UserCreate, UserUpdate, ItemCreate, ItemUpdate

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ============== User CRUD ==============

def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get a user by ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get a user by email."""
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get all users with pagination."""
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user."""
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """Update a user."""
    db_user = get_user(db, user_id)
    if not db_user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user."""
    db_user = get_user(db, user_id)
    if not db_user:
        return False

    db.delete(db_user)
    db.commit()
    return True


# ============== Item CRUD ==============

def get_item(db: Session, item_id: int) -> Optional[Item]:
    """Get an item by ID."""
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
    """Get all items for a specific user."""
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
