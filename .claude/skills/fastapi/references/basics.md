# FastAPI Basics

Complete guide for beginners - from installation to your first API.

---

## Installation with uv

### Initialize Project (Recommended)
```bash
# Create and enter project directory
mkdir my-fastapi-app && cd my-fastapi-app

# Initialize uv project
uv init

# Add FastAPI with standard extras
uv add fastapi[standard]
```

This includes:
- `fastapi` - The framework
- `uvicorn` - ASGI server
- `pydantic` - Data validation
- Other useful dependencies

### Minimal Installation
```bash
uv add fastapi uvicorn
```

---

## Hello World

### Simplest FastAPI App

Create `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

### Run the Application

**Development mode (auto-reload):**
```bash
uv run fastapi dev main.py
```

**Production mode:**
```bash
uv run fastapi run main.py
```

**Using uvicorn directly:**
```bash
uv run uvicorn main:app --reload
```

### Access Your API

- API: http://127.0.0.1:8000
- Swagger Docs: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## HTTP Methods

### GET - Retrieve Data
```python
@app.get("/items")
def get_items():
    return {"items": ["item1", "item2"]}
```

### POST - Create Data
```python
@app.post("/items")
def create_item():
    return {"message": "Item created"}
```

### PUT - Update Data (Full)
```python
@app.put("/items/{item_id}")
def update_item(item_id: int):
    return {"message": f"Item {item_id} updated"}
```

### PATCH - Update Data (Partial)
```python
@app.patch("/items/{item_id}")
def patch_item(item_id: int):
    return {"message": f"Item {item_id} patched"}
```

### DELETE - Remove Data
```python
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": f"Item {item_id} deleted"}
```

---

## Path Parameters

Path parameters are parts of the URL path.

### Basic Path Parameter
```python
@app.get("/users/{user_id}")
def read_user(user_id: int):
    return {"user_id": user_id}
```

### Multiple Path Parameters
```python
@app.get("/users/{user_id}/posts/{post_id}")
def read_user_post(user_id: int, post_id: int):
    return {"user_id": user_id, "post_id": post_id}
```

### Path Parameter with Validation
```python
from fastapi import Path

@app.get("/items/{item_id}")
def read_item(
    item_id: int = Path(..., title="Item ID", ge=1, le=1000)
):
    return {"item_id": item_id}
```

### Predefined Values (Enum)
```python
from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
def get_model(model_name: ModelName):
    return {"model": model_name}
```

---

## Query Parameters

Query parameters come after `?` in the URL.

### Basic Query Parameter
```python
# URL: /items?skip=0&limit=10
@app.get("/items")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

### Optional Query Parameter
```python
from typing import Optional

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}
```

### Required Query Parameter
```python
@app.get("/items")
def read_items(q: str):  # No default = required
    return {"q": q}
```

### Query Parameter Validation
```python
from fastapi import Query

@app.get("/items")
def read_items(
    q: str = Query(
        default=None,
        min_length=3,
        max_length=50,
        pattern="^[a-z]+$"
    )
):
    return {"q": q}
```

### List Query Parameters
```python
from typing import List

# URL: /items?tags=tag1&tags=tag2
@app.get("/items")
def read_items(tags: List[str] = Query(default=[])):
    return {"tags": tags}
```

---

## Request Body

For sending data to the API (POST, PUT, PATCH).

### Simple Request Body
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

@app.post("/items")
def create_item(item: Item):
    return {"item_name": item.name, "item_price": item.price}
```

### Request Body + Path + Query
```python
@app.put("/items/{item_id}")
def update_item(
    item_id: int,           # Path parameter
    item: Item,             # Request body
    q: str = None           # Query parameter
):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result["q"] = q
    return result
```

---

## Response Handling

### Status Codes
```python
from fastapi import status

@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    return item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    return None
```

### Response Model
```python
class ItemResponse(BaseModel):
    name: str
    price: float

@app.get("/items/{item_id}", response_model=ItemResponse)
def read_item(item_id: int):
    # Even if we return more fields, only name and price are sent
    return {"name": "Foo", "price": 50.0, "secret": "hidden"}
```

### Custom Response
```python
from fastapi.responses import JSONResponse

@app.get("/custom")
def custom_response():
    return JSONResponse(
        content={"message": "Custom response"},
        status_code=200,
        headers={"X-Custom-Header": "value"}
    )
```

---

## Error Handling

### HTTPException
```python
from fastapi import HTTPException

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )
    return items_db[item_id]
```

### Custom Exception Handler
```python
from fastapi import Request
from fastapi.responses import JSONResponse

class CustomException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something wrong."}
    )
```

---

## App Configuration

### Basic Configuration
```python
app = FastAPI(
    title="My API",
    description="API description here",
    version="1.0.0"
)
```

### Full Configuration
```python
app = FastAPI(
    title="My Awesome API",
    description="This is a very fancy API",
    version="2.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Support Team",
        "url": "http://example.com/contact/",
        "email": "support@example.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    docs_url="/documentation",
    redoc_url="/redoc",
    openapi_url="/api/openapi.json"
)
```

---

## Complete Beginner Example

```python
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="My First API", version="1.0.0")

# In-memory database
items_db = {}

# Models
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float

# Routes
@app.get("/")
def root():
    return {"message": "Welcome to My First API!"}

@app.get("/items", response_model=List[ItemResponse])
def list_items(skip: int = 0, limit: int = Query(default=10, le=100)):
    items = list(items_db.values())
    return items[skip : skip + limit]

@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: Item):
    item_id = len(items_db) + 1
    items_db[item_id] = {"id": item_id, **item.dict()}
    return items_db[item_id]

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return None
```

Run with: `uv run fastapi dev main.py`
