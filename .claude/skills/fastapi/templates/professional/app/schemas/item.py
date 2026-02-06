"""Item schemas."""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class ItemBase(BaseModel):
    """Base item schema."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    is_available: bool = True


class ItemCreate(ItemBase):
    """Item creation schema."""
    pass


class ItemUpdate(BaseModel):
    """Item update schema."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    is_available: Optional[bool] = None


class ItemResponse(ItemBase):
    """Item response schema."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: Optional[int]
    created_at: datetime
