# tests/test_users.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, engine
from sqlmodel import SQLModel, Session
from app.crud import create_user

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    SQLModel.metadata.create_all(engine)
    # buat admin dan staff seed
    with Session(engine) as s:
        admin = create_user(s, "admin001", "admin@example.com", "Admin@123", "admin")
        staff = create_user(s, "staff01", "staff@example.com", "Staff@123", "staff")
    yield
    SQLModel.metadata.drop_all(engine)

def test_create_user_success():
    payload = {
        "username": "newuser1",
        "email": "newuser1@example.com",
        "password": "Aa1!aaaa",
        "role": "staff"
    }
    r = client.post("/users/", json=payload)
    assert r.status_code == 201
    assert r.json()["username"] == "newuser1"

def test_read_all_admin_success():
    headers = {"X-Username": "admin001", "X-Role": "admin"}
    r = client.get("/users/", headers=headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_read_all_staff_forbidden():
    headers = {"X-Username": "staff01", "X-Role": "staff"}
    r = client.get("/users/", headers=headers)
    assert r.status_code == 403

def test_staff_read_own_success():
    headers = {"X-Username": "staff01", "X-Role": "staff"}
    # assume staff id is known (look up by username or call /users/me)
    r = client.get("/users/me", headers=headers)
    assert r.status_code == 200
    assert r.json()["username"] == "staff01"
