# Testing FastAPI Applications

Comprehensive guide to testing with pytest and TestClient.

---

## Setup

### Installation
```bash
uv add --dev pytest
uv add --dev httpx          # Required for TestClient
uv add --dev pytest-asyncio # For async tests
```

### Project Structure
```
app/
├── main.py
├── routers/
├── models/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_main.py
│   └── test_users.py
└── pytest.ini
```

### pytest.ini
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
asyncio_mode = auto
```

---

## Basic Testing

### Simple Test
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_read_item():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_create_item():
    response = client.post(
        "/items",
        json={"name": "Test Item", "price": 10.5}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Item"
```

---

## Using Fixtures

### conftest.py
```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with overridden database."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
```

### Using Fixtures in Tests
```python
def test_create_user(client, db_session):
    response = client.post(
        "/users",
        json={"email": "test@example.com", "name": "Test User", "password": "secret"}
    )
    assert response.status_code == 201

    # Verify in database
    from models import User
    user = db_session.query(User).filter(User.email == "test@example.com").first()
    assert user is not None
    assert user.name == "Test User"
```

---

## Testing with Authentication

### Auth Fixture
```python
@pytest.fixture
def auth_headers(client):
    """Get authentication headers for a test user."""
    # Create user
    client.post(
        "/users",
        json={"email": "test@example.com", "name": "Test", "password": "testpass"}
    )

    # Login
    response = client.post(
        "/token",
        data={"username": "test@example.com", "password": "testpass"}
    )
    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}

def test_protected_route(client, auth_headers):
    response = client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_protected_route_unauthorized(client):
    response = client.get("/users/me")
    assert response.status_code == 401
```

### Mock Current User
```python
from unittest.mock import patch

@pytest.fixture
def mock_current_user():
    return {"id": 1, "email": "test@example.com", "name": "Test User"}

def test_with_mocked_user(client, mock_current_user):
    from auth import get_current_user

    app.dependency_overrides[get_current_user] = lambda: mock_current_user

    response = client.get("/users/me")
    assert response.status_code == 200

    app.dependency_overrides.clear()
```

---

## Async Testing

### Async Test Functions
```python
import pytest
from httpx import AsyncClient
from main import app

@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/async-items")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_async_create():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/items",
            json={"name": "Async Item", "price": 25.0}
        )
    assert response.status_code == 201
```

---

## Testing Different Scenarios

### Testing Query Parameters
```python
def test_list_items_with_pagination(client):
    # Create multiple items first
    for i in range(15):
        client.post("/items", json={"name": f"Item {i}", "price": i * 10})

    # Test pagination
    response = client.get("/items?skip=0&limit=5")
    assert response.status_code == 200
    assert len(response.json()) == 5

    response = client.get("/items?skip=10&limit=5")
    assert response.status_code == 200
    assert len(response.json()) == 5
```

### Testing Path Parameters
```python
def test_get_item_not_found(client):
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_get_item_invalid_id(client):
    response = client.get("/items/invalid")
    assert response.status_code == 422  # Validation error
```

### Testing Request Body Validation
```python
def test_create_item_invalid_price(client):
    response = client.post(
        "/items",
        json={"name": "Test", "price": -10}  # Negative price
    )
    assert response.status_code == 422

def test_create_item_missing_field(client):
    response = client.post(
        "/items",
        json={"name": "Test"}  # Missing price
    )
    assert response.status_code == 422
```

### Testing Headers
```python
def test_custom_header(client):
    response = client.get(
        "/items",
        headers={"X-Custom-Header": "custom-value"}
    )
    assert response.status_code == 200

def test_api_key_authentication(client):
    response = client.get(
        "/external/data",
        headers={"X-API-Key": "valid-api-key"}
    )
    assert response.status_code == 200

    response = client.get("/external/data")
    assert response.status_code == 401
```

---

## Mocking External Services

### Mock HTTP Calls
```python
from unittest.mock import patch, MagicMock

def test_external_api_call(client):
    mock_response = MagicMock()
    mock_response.json.return_value = {"data": "mocked"}
    mock_response.status_code = 200

    with patch("httpx.get", return_value=mock_response):
        response = client.get("/fetch-external")
        assert response.status_code == 200
        assert response.json()["data"] == "mocked"
```

### Mock Database Queries
```python
def test_with_mocked_db(client):
    mock_users = [
        {"id": 1, "name": "User 1"},
        {"id": 2, "name": "User 2"}
    ]

    with patch("crud.get_users", return_value=mock_users):
        response = client.get("/users")
        assert response.status_code == 200
        assert len(response.json()) == 2
```

---

## Test Organization

### Testing CRUD Operations
```python
# tests/test_users.py

class TestUserCRUD:
    """Test user CRUD operations."""

    def test_create_user(self, client):
        response = client.post(
            "/users",
            json={"email": "new@example.com", "name": "New User", "password": "pass"}
        )
        assert response.status_code == 201
        self.created_user_id = response.json()["id"]

    def test_read_user(self, client):
        # First create
        create_response = client.post(
            "/users",
            json={"email": "read@example.com", "name": "Read User", "password": "pass"}
        )
        user_id = create_response.json()["id"]

        # Then read
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 200
        assert response.json()["email"] == "read@example.com"

    def test_update_user(self, client):
        # Create
        create_response = client.post(
            "/users",
            json={"email": "update@example.com", "name": "Update User", "password": "pass"}
        )
        user_id = create_response.json()["id"]

        # Update
        response = client.patch(
            f"/users/{user_id}",
            json={"name": "Updated Name"}
        )
        assert response.status_code == 200
        assert response.json()["name"] == "Updated Name"

    def test_delete_user(self, client):
        # Create
        create_response = client.post(
            "/users",
            json={"email": "delete@example.com", "name": "Delete User", "password": "pass"}
        )
        user_id = create_response.json()["id"]

        # Delete
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 204

        # Verify deleted
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 404
```

---

## Coverage Report

### Installation
```bash
uv add --dev pytest-cov
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html
```

### View Report
Open `htmlcov/index.html` in browser.

---

## Complete Test Example

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture
def sample_item():
    return {"name": "Test Item", "description": "A test item", "price": 29.99}

# tests/test_items.py
def test_create_item(client, sample_item):
    response = client.post("/items", json=sample_item)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_item["name"]
    assert "id" in data

def test_read_items_empty(client):
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == []

def test_read_items(client, sample_item):
    client.post("/items", json=sample_item)
    response = client.get("/items")
    assert response.status_code == 200
    assert len(response.json()) == 1
```
