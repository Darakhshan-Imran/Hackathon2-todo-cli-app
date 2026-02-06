"""Pydantic schemas for request/response validation."""

from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime


# ============== User Schemas ==============

class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    """Schema for creating a user."""
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=1, max_length=100)


class UserResponse(UserBase):
    """Schema for user response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime


# ============== Item Schemas ==============

class ItemBase(BaseModel):
    """Base item schema."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    is_available: bool = True


class ItemCreate(ItemBase):
    """Schema for creating an item."""
    pass


class ItemUpdate(BaseModel):
    """Schema for updating an item."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    is_available: Optional[bool] = None


class ItemResponse(ItemBase):
    """Schema for item response."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: Optional[int]
    created_at: datetime


class ItemWithOwner(ItemResponse):
    """Schema for item with owner details."""
    owner: Optional[UserResponse] = None


# ============== User with Items ==============

class UserWithItems(UserResponse):
    """Schema for user with their items."""
    items: List[ItemResponse] = []
