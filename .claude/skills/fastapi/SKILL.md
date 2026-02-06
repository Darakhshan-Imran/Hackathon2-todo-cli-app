---
name: fastapi
description: Comprehensive FastAPI skill for building modern Python APIs - from simple Hello World to production-ready applications. Covers routing, Pydantic models, database integration, authentication, testing, and deployment. Use this skill when creating, debugging, or enhancing FastAPI projects.
---

# FastAPI Development Skill

Build modern, fast Python APIs with FastAPI - from beginner to professional level.

---

## WHEN TO USE THIS SKILL

**Use this skill when:**

| Level | Use Case | Reference File |
|-------|----------|----------------|
| **Beginner** | Hello World, basic routes, installation | `references/basics.md` |
| **Beginner** | Path parameters, query parameters | `references/basics.md` |
| **Intermediate** | Request/response models with Pydantic | `references/models.md` |
| **Intermediate** | Database integration (SQLAlchemy) | `references/database.md` |
| **Intermediate** | CRUD operations | `references/database.md` |
| **Advanced** | Authentication (JWT, OAuth2) | `references/authentication.md` |
| **Advanced** | Testing with pytest | `references/testing.md` |
| **Advanced** | Docker & production deployment | `references/deployment.md` |
| **All Levels** | Project structure & best practices | `references/best-practices.md` |

---

## QUICK START

### 1. Initialize Project with uv

```bash
# Create project directory
mkdir my-fastapi-app && cd my-fastapi-app

# Initialize uv project
uv init

# Add FastAPI dependency
uv add fastapi[standard]
```

### 2. Create Your First App

Create `main.py`:
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

### 3. Run the Server

```bash
uv run fastapi dev main.py
```

Visit: `http://127.0.0.1:8000/docs` for interactive API documentation.

---

## HOW TO USE THIS SKILL

### Step 1: Identify the Task Level

| If the user wants to... | Level | Go to |
|------------------------|-------|-------|
| Create a simple API, learn basics | Beginner | `references/basics.md` |
| Add data validation, complex responses | Intermediate | `references/models.md` |
| Connect to a database | Intermediate | `references/database.md` |
| Add login/security | Advanced | `references/authentication.md` |
| Write tests | Advanced | `references/testing.md` |
| Deploy to production | Advanced | `references/deployment.md` |
| Structure a large project | Any | `references/best-practices.md` |

### Step 2: Load the Appropriate Reference

Read the corresponding file from the `references/` directory and follow the patterns.

### Step 3: Use Templates (Optional)

For new projects, use templates from `templates/` directory:
- `templates/minimal/` - Single file, minimal setup
- `templates/standard/` - Standard project structure
- `templates/professional/` - Full production-ready structure

---

## REFERENCE FILES

| File | Description |
|------|-------------|
| [basics.md](references/basics.md) | Installation, Hello World, routes, parameters |
| [models.md](references/models.md) | Pydantic models, validation, serialization |
| [database.md](references/database.md) | SQLAlchemy, CRUD, migrations |
| [authentication.md](references/authentication.md) | JWT, OAuth2, security |
| [testing.md](references/testing.md) | pytest, TestClient, fixtures |
| [deployment.md](references/deployment.md) | Docker, Gunicorn, production setup |
| [best-practices.md](references/best-practices.md) | Project structure, patterns, tips |

---

## COMMON PATTERNS

### Basic GET Endpoint
```python
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

### POST with Pydantic Model
```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
def create_item(item: Item):
    return item
```

### Async Endpoint
```python
@app.get("/async-items/")
async def read_async_items():
    return {"items": ["item1", "item2"]}
```

### With Dependencies
```python
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()
```

---

## KEYWORDS

FastAPI, Python API, REST API, Pydantic, SQLAlchemy, JWT, OAuth2, async, CRUD, OpenAPI, Swagger, uvicorn, deployment, Docker
