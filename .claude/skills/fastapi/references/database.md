# Database Integration with FastAPI

SQLAlchemy integration, CRUD operations, and database best practices.

---

## Setup

### Installation
```bash
uv add sqlalchemy
uv add psycopg2-binary  # For PostgreSQL
# OR
uv add aiosqlite        # For async SQLite
```

### Database Configuration

**database.py**
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite (Development)
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # SQLite only
)

# PostgreSQL (Production)
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## SQLAlchemy Models

### Basic Model
```python
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

### Model with Relationships
```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    name = Column(String(100))

    # One-to-Many: User has many posts
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Many-to-One: Post belongs to User
    author = relationship("User", back_populates="posts")
```

### Many-to-Many Relationship
```python
from sqlalchemy import Table, Column, Integer, ForeignKey

# Association table
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(200))

    tags = relationship("Tag", secondary=post_tags, back_populates="posts")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)

    posts = relationship("Post", secondary=post_tags, back_populates="tags")
```

---

## Pydantic Schemas

### Separate Models for API
```python
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

# Base schema (shared fields)
class UserBase(BaseModel):
    email: str
    name: str

# Create schema (input)
class UserCreate(UserBase):
    password: str

# Update schema (partial update)
class UserUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None

# Response schema (output)
class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime

# With relationships
class UserWithPosts(UserResponse):
    posts: List['PostResponse'] = []
```

---

## CRUD Operations

### Create (crud.py)
```python
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate

def create_user(db: Session, user: UserCreate) -> User:
    hashed_password = hash_password(user.password)
    db_user = User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

### Read
```python
from typing import Optional, List

def get_user(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()
```

### Update
```python
from schemas import UserUpdate

def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user
```

### Delete
```python
def delete_user(db: Session, user_id: int) -> bool:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return False

    db.delete(db_user)
    db.commit()
    return True
```

---

## FastAPI Endpoints

### Complete Router
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import crud
from schemas import UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    return crud.create_user(db=db, user=user)

@router.get("/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id=user_id, user_update=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None
```

---

## Advanced Queries

### Filtering
```python
def get_users_filtered(
    db: Session,
    is_active: bool = None,
    name_contains: str = None
) -> List[User]:
    query = db.query(User)

    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    if name_contains:
        query = query.filter(User.name.ilike(f"%{name_contains}%"))

    return query.all()
```

### Ordering
```python
from sqlalchemy import desc

def get_users_ordered(db: Session, order_by: str = "created_at") -> List[User]:
    query = db.query(User)

    if order_by.startswith("-"):
        query = query.order_by(desc(getattr(User, order_by[1:])))
    else:
        query = query.order_by(getattr(User, order_by))

    return query.all()
```

### Pagination
```python
from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar('T')

class Page(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

def get_users_paginated(db: Session, page: int = 1, size: int = 10) -> Page[User]:
    total = db.query(User).count()
    items = db.query(User).offset((page - 1) * size).limit(size).all()

    return Page(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )
```

### Eager Loading (Avoid N+1)
```python
from sqlalchemy.orm import joinedload, selectinload

def get_user_with_posts(db: Session, user_id: int) -> User:
    return db.query(User)\
        .options(selectinload(User.posts))\
        .filter(User.id == user_id)\
        .first()

def get_all_users_with_posts(db: Session) -> List[User]:
    return db.query(User)\
        .options(selectinload(User.posts))\
        .all()
```

---

## Async Database (Optional)

### Async Setup
```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

ASYNC_DATABASE_URL = "sqlite+aiosqlite:///./app.db"

async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
```

### Async CRUD
```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

async def get_user_async(db: AsyncSession, user_id: int) -> Optional[User]:
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalar_one_or_none()

async def create_user_async(db: AsyncSession, user: UserCreate) -> User:
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
```

### Async Endpoint
```python
@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: AsyncSession = Depends(get_async_db)):
    user = await get_user_async(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

---

## Database Migrations with Alembic

### Installation
```bash
uv add alembic
```

### Initialize
```bash
alembic init alembic
```

### Configure (alembic/env.py)
```python
from models import Base
from database import SQLALCHEMY_DATABASE_URL

config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)
target_metadata = Base.metadata
```

### Create Migration
```bash
alembic revision --autogenerate -m "Create users table"
```

### Run Migration
```bash
alembic upgrade head
```

### Rollback
```bash
alembic downgrade -1
```

---

## Complete Project Structure

```
app/
├── main.py
├── database.py
├── models/
│   ├── __init__.py
│   └── user.py
├── schemas/
│   ├── __init__.py
│   └── user.py
├── crud/
│   ├── __init__.py
│   └── user.py
├── routers/
│   ├── __init__.py
│   └── users.py
└── alembic/
    ├── env.py
    └── versions/
```

### main.py
```python
from fastapi import FastAPI
from database import engine, Base
from routers import users

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="My API")

app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Welcome to My API"}
```
