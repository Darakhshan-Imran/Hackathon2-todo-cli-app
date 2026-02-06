# FastAPI Best Practices

Project structure, coding patterns, and professional tips.

---

## Project Structures

### Minimal (Single File)
Best for: Learning, prototypes, microservices
```
project/
├── main.py
├── pyproject.toml
├── uv.lock
└── .env
```

### Standard (Small to Medium Projects)
Best for: Small APIs, personal projects
```
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── routers/
│       ├── __init__.py
│       ├── users.py
│       └── items.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_users.py
├── pyproject.toml
├── uv.lock
├── .env
└── README.md
```

### Professional (Large Projects)
Best for: Production applications, team projects
```
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── dependencies.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── migrations/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── user.py
│   │   └── item.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       ├── endpoints/
│   │       │   ├── users.py
│   │       │   └── items.py
│   └── services/
│       ├── __init__.py
│       └── email.py
├── tests/
├── alembic/
├── docker/
├── scripts/
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
├── .env.example
└── README.md
```

---

## Code Organization Patterns

### Router Organization
```python
# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.endpoints import users, items, auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
```

### Main Application
```python
# app/main.py
from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_V1_STR)
```

---

## Dependency Injection Patterns

### Database Dependency
```python
# app/api/deps.py
from typing import Generator
from app.db.database import SessionLocal

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Current User Dependency
```python
# app/api/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import verify_token
from app.crud import crud_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user_id = verify_token(token)
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def get_current_active_user(
    current_user = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```

### Reusable Dependencies
```python
# Pagination dependency
from fastapi import Query

def pagination_params(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    return {"skip": skip, "limit": limit}

@router.get("/items")
def list_items(pagination: dict = Depends(pagination_params)):
    return get_items(skip=pagination["skip"], limit=pagination["limit"])
```

---

## CRUD Base Pattern

### Generic CRUD Class
```python
# app/crud/base.py
from typing import Generic, TypeVar, Type, Optional, List
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_data = obj_in.model_dump()
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
```

### Using CRUD Base
```python
# app/crud/user.py
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

crud_user = CRUDUser(User)
```

---

## Error Handling Patterns

### Custom Exception Classes
```python
# app/core/exceptions.py
from fastapi import HTTPException, status

class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Not authenticated"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
```

### Global Exception Handler
```python
# app/main.py
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal server error",
            "detail": str(exc) if settings.DEBUG else None
        }
    )
```

---

## Response Patterns

### Consistent API Responses
```python
# app/schemas/response.py
from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel

T = TypeVar('T')

class ResponseModel(BaseModel, Generic[T]):
    success: bool = True
    message: str = ""
    data: Optional[T] = None

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

# Usage
@router.get("/users/{user_id}", response_model=ResponseModel[UserResponse])
def get_user(user_id: int):
    user = crud_user.get(db, user_id)
    return ResponseModel(data=user, message="User retrieved successfully")
```

---

## Configuration Management

### Settings Class
```python
# app/core/config.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API
    PROJECT_NAME: str = "My FastAPI Project"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

---

## Performance Tips

### Use Async When Appropriate
```python
# Good: Async for I/O operations
@router.get("/items")
async def get_items(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Item))
    return result.scalars().all()

# Good: Sync for CPU-bound operations
@router.get("/compute")
def compute_heavy():
    return heavy_computation()
```

### Background Tasks
```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Send email logic
    pass

@router.post("/users")
async def create_user(
    user: UserCreate,
    background_tasks: BackgroundTasks
):
    new_user = crud_user.create(db, user)
    background_tasks.add_task(send_email, user.email, "Welcome!")
    return new_user
```

### Caching
```python
from functools import lru_cache

@lru_cache()
def get_settings():
    return Settings()

# Or use Redis for distributed caching
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

@router.get("/expensive")
@cache(expire=60)
async def expensive_operation():
    return await slow_database_query()
```

---

## Documentation Tips

### Add Examples
```python
class Item(BaseModel):
    name: str = Field(..., example="Widget")
    price: float = Field(..., example=29.99)
    description: str = Field(None, example="A useful widget")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Fancy Widget",
                "price": 99.99,
                "description": "A very fancy widget"
            }
        }
    )
```

### Document Endpoints
```python
@router.get(
    "/items/{item_id}",
    response_model=ItemResponse,
    summary="Get a single item",
    description="Retrieve an item by its ID. Returns 404 if not found.",
    responses={
        200: {"description": "Item found"},
        404: {"description": "Item not found"}
    }
)
def get_item(item_id: int):
    """
    Get an item by ID.

    - **item_id**: The unique identifier of the item
    """
    pass
```

---

## Common Mistakes to Avoid

### 1. Not Using Dependency Injection
```python
# Bad
@router.get("/users")
def get_users():
    db = SessionLocal()  # Creates new connection each time
    users = db.query(User).all()
    db.close()
    return users

# Good
@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

### 2. Exposing Sensitive Data
```python
# Bad - Returns password
@router.get("/users/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == id).first()

# Good - Uses response model
@router.get("/users/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == id).first()
```

### 3. N+1 Query Problem
```python
# Bad - Causes N+1 queries
@router.get("/users")
def get_users_with_posts(db: Session = Depends(get_db)):
    users = db.query(User).all()
    for user in users:
        _ = user.posts  # Triggers additional query for each user
    return users

# Good - Eager loading
@router.get("/users")
def get_users_with_posts(db: Session = Depends(get_db)):
    return db.query(User).options(selectinload(User.posts)).all()
```

### 4. Blocking Async Event Loop
```python
# Bad - Blocks event loop
@router.get("/data")
async def get_data():
    time.sleep(5)  # Blocks!
    return {"data": "result"}

# Good - Use async sleep or run in thread
@router.get("/data")
async def get_data():
    await asyncio.sleep(5)
    return {"data": "result"}
```
