# Pydantic Models in FastAPI

Data validation, serialization, and schema generation with Pydantic.

---

## Basic Models

### Simple Model
```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True
```

### Using Models in Endpoints
```python
@app.post("/users")
def create_user(user: User):
    return user

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    return {"id": user_id, "name": "John", "email": "john@example.com"}
```

---

## Field Types

### Common Types
```python
from typing import Optional, List, Dict
from datetime import datetime, date
from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    price: float
    quantity: int
    tags: List[str] = []
    metadata: Dict[str, str] = {}
    description: Optional[str] = None
    created_at: datetime
    release_date: date
```

### Union Types (Multiple Possible Types)
```python
from typing import Union

class Item(BaseModel):
    price: Union[int, float]
    description: Union[str, None] = None
```

### Literal Types (Fixed Values)
```python
from typing import Literal

class Order(BaseModel):
    status: Literal["pending", "processing", "shipped", "delivered"]
```

---

## Field Validation

### Using Field()
```python
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    quantity: int = Field(default=1, ge=0, le=1000)
    description: str = Field(default=None, max_length=500)
```

### Field Parameters
| Parameter | Description |
|-----------|-------------|
| `...` | Required field (no default) |
| `default` | Default value |
| `min_length` | Minimum string length |
| `max_length` | Maximum string length |
| `gt` | Greater than |
| `ge` | Greater than or equal |
| `lt` | Less than |
| `le` | Less than or equal |
| `pattern` | Regex pattern |
| `description` | Field description for docs |
| `example` | Example value for docs |

### Custom Validators
```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    name: str
    email: str
    age: int

    @field_validator('name')
    @classmethod
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.title()

    @field_validator('email')
    @classmethod
    def email_must_contain_at(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower()

    @field_validator('age')
    @classmethod
    def age_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Age must be positive')
        return v
```

### Model Validators (Cross-field)
```python
from pydantic import BaseModel, model_validator

class DateRange(BaseModel):
    start_date: date
    end_date: date

    @model_validator(mode='after')
    def check_dates(self):
        if self.start_date > self.end_date:
            raise ValueError('start_date must be before end_date')
        return self
```

---

## Nested Models

### Basic Nesting
```python
class Address(BaseModel):
    street: str
    city: str
    country: str
    zip_code: str

class User(BaseModel):
    id: int
    name: str
    address: Address
```

### List of Nested Models
```python
class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price: float

class Order(BaseModel):
    id: int
    customer_id: int
    items: List[OrderItem]
    total: float
```

### Self-referencing Models
```python
from typing import Optional, List

class Category(BaseModel):
    id: int
    name: str
    parent: Optional['Category'] = None
    children: List['Category'] = []

Category.model_rebuild()  # Required for self-reference
```

---

## Request/Response Models

### Separate Input and Output Models
```python
# Input model - what client sends
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

# Output model - what client receives (no password!)
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool

# Database model representation
class UserInDB(BaseModel):
    id: int
    name: str
    email: str
    hashed_password: str
    is_active: bool

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    # Password is hashed, stored in DB
    # Returns UserResponse (no password exposed)
    pass
```

### Update Models (Partial Updates)
```python
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

@app.patch("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate):
    stored_data = get_user(user_id)
    update_data = user.dict(exclude_unset=True)
    updated_user = stored_data.copy(update=update_data)
    return updated_user
```

---

## Model Configuration

### Using model_config
```python
from pydantic import BaseModel, ConfigDict

class User(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,  # Strip whitespace from strings
        str_min_length=1,           # Minimum string length
        from_attributes=True,        # Allow ORM mode (from SQLAlchemy)
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "John Doe",
                "email": "john@example.com"
            }
        }
    )

    id: int
    name: str
    email: str
```

### ORM Mode (for SQLAlchemy)
```python
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str

# Now you can do:
# user_response = UserResponse.model_validate(sqlalchemy_user_object)
```

---

## Model Methods

### Serialization
```python
user = User(id=1, name="John", email="john@example.com")

# To dictionary
user.model_dump()
# {'id': 1, 'name': 'John', 'email': 'john@example.com'}

# To JSON string
user.model_dump_json()
# '{"id": 1, "name": "John", "email": "john@example.com"}'

# Exclude fields
user.model_dump(exclude={'email'})

# Include only specific fields
user.model_dump(include={'id', 'name'})

# Exclude None values
user.model_dump(exclude_none=True)

# Exclude unset values
user.model_dump(exclude_unset=True)
```

### Validation
```python
# Validate dict
user = User.model_validate({'id': 1, 'name': 'John', 'email': 'john@example.com'})

# Validate JSON string
user = User.model_validate_json('{"id": 1, "name": "John", "email": "john@example.com"}')

# From ORM object
user = User.model_validate(orm_user, from_attributes=True)
```

---

## Generic Models

### Paginated Response
```python
from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int

@app.get("/users", response_model=PaginatedResponse[UserResponse])
def list_users(page: int = 1, size: int = 10):
    users = get_users(page, size)
    total = count_users()
    return PaginatedResponse(
        items=users,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )
```

### API Response Wrapper
```python
class APIResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    message: str = ""
    errors: List[str] = []

@app.get("/users/{user_id}", response_model=APIResponse[UserResponse])
def get_user(user_id: int):
    user = find_user(user_id)
    if not user:
        return APIResponse(success=False, message="User not found")
    return APIResponse(success=True, data=user)
```

---

## Complete Example

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime

app = FastAPI()

# Models
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    category: str

    @field_validator('name')
    @classmethod
    def name_must_be_valid(cls, v):
        return v.strip().title()

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None

class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime

# In-memory storage
products_db: dict = {}

# Endpoints
@app.post("/products", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate):
    product_id = len(products_db) + 1
    now = datetime.now()
    db_product = {
        "id": product_id,
        **product.model_dump(),
        "created_at": now,
        "updated_at": now
    }
    products_db[product_id] = db_product
    return db_product

@app.get("/products", response_model=List[ProductResponse])
def list_products(category: Optional[str] = None):
    products = list(products_db.values())
    if category:
        products = [p for p in products if p["category"] == category]
    return products

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return products_db[product_id]

@app.patch("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductUpdate):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")

    stored = products_db[product_id]
    update_data = product.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        stored[key] = value
    stored["updated_at"] = datetime.now()

    return stored
```
