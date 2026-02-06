"""User schemas."""

from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    """User creation schema."""
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    """User update schema."""
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, min_length=1, max_length=100)


class UserResponse(UserBase):
    """User response schema."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime
