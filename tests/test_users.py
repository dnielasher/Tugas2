# tests/test_users.py
# tests/test_users.py

import sys
import os

# Menambahkan direktori root proyek ke path Python
# Ini memungkinkan 'from main import app' berfungsi dengan benar
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Kode Anda yang sudah ada dimulai dari sini
from fastapi.testclient import TestClient
import pytest
from main import app
#... sisa kode Anda...

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db, engine
from sqlmodel import SQLModel, Session, select
from app.crud import create_user, get_user_by_username
from app.models import Role

client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    # create fresh DB
    SQLModel.metadata.create_all(engine)
    # seed admin and staff
    with Session(engine) as s:
        # create admin
        if not get_user_by_username(s, "admin001"):
            create_user(s, "admin001", "admin@example.com", "Admin@123", Role.admin)
        if not get_user_by_username(s, "staff01"):
            create_user(s, "staff01", "staff@example.com", "Staff@123", Role.staff)
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
    body = r.json()
    assert body["username"] == "newuser1"
    assert "hashed_password" not in body

def test_create_user_bad_username():
    payload = {
        "username": "BAD",
        "email": "baduser@example.com",
        "password": "Aa1!aaaa",
        "role": "staff"
    }
    r = client.post("/users/", json=payload)
    assert r.status_code == 422

def test_read_all_admin_success():
    headers = {"X-Username": "admin001", "X-Role": "admin"}
    r = client.get("/users/", headers=headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert any(u["username"] == "admin001" for u in r.json())

def test_read_all_staff_forbidden():
    headers = {"X-Username": "staff01", "X-Role": "staff"}
    r = client.get("/users/", headers=headers)
    assert r.status_code == 403

def test_staff_read_own_success():
    headers = {"X-Username": "staff01", "X-Role": "staff"}
    r = client.get("/users/me", headers=headers)
    assert r.status_code == 200
    assert r.json()["username"] == "staff01"

def test_admin_update_user_success():
    # admin updates staff email
    headers = {"X-Username": "admin001", "X-Role": "admin"}
    # find staff id by calling read all
    r = client.get("/users/", headers=headers)
    staff = next(u for u in r.json() if u["username"] == "staff01")
    payload = {"email": "staff01new@example.com"}
    r2 = client.put(f"/users/{staff['id']}", json=payload, headers=headers)
    assert r2.status_code == 200
    assert r2.json()["email"] == "staff01new@example.com"

def test_admin_delete_user_success():
    headers = {"X-Username": "admin001", "X-Role": "admin"}
    # create a temp user
    payload = {
        "username": "todelete1",
        "email": "todelete1@example.com",
        "password": "Aa1!aaaa",
        "role": "staff"
    }
    r = client.post("/users/", json=payload)
    assert r.status_code == 201
    user_id = r.json()["id"]
    r2 = client.delete(f"/users/{user_id}", headers=headers)
    assert r2.status_code == 204
    # ensure deleted
    r3 = client.get(f"/users/{user_id}", headers=headers)
    assert r3.status_code == 404
