from http import client
from fastapi.testclient import TestClient

from main import app
from src.address.models.address import Address
from src.databaseSimulation.databases import addresses_db

client = TestClient(app)

def test_get_addresses_empty():
    response = client.get("/addresses/")
    assert response.status_code == 404
    assert response.json() == {"detail": "No addresses found"}


def test_get_addresses_with_data():
    # Agrega direcciones ficticias a addresses_db
    address_data = {
        "address_id": 1,
        "address_1": "123 Main St",
        "city": "City",
        "state": "State",
        "zip": "12345",
        "country": "Country"
    }
    address_instance = Address(**address_data)
    addresses_db.append(address_instance)
    response = client.get("/addresses/")
    assert response.status_code == 200
    assert len(response.json()) == len(addresses_db)


def test_get_addresses_with_data():
    valid_address_data = {
        "address_id": 1,
        "address_1": "123 Main St",
        "address_2": "",
        "city": "City",
        "state": "State",
        "zip": "12345",
        "country": "Country"
    }
    valid_address = Address(**valid_address_data)
    addresses_db.append(valid_address)
    response = client.get("/addresses/")
    assert response.status_code == 200
    assert valid_address.dict() in response.json()


def test_create_address_with_nonexistent_user():
    email = "nonexistent@example.com"
    address_data = {"address_1": "123 Main St", "city": "City", "state": "State", "zip": "12345", "country": "Country"}
    response = client.post(f"/addresses/?email={email}", json=address_data)
    assert response.status_code == 422


def test_create_address_with_invalid_data():
    email = "user@example.com"
    invalid_address_data = {"address_1": "", "city": "", "state": "", "zip": "12345", "country": "Country"}
    response = client.post(f"/addresses/?email={email}", json=invalid_address_data)
    assert response.status_code == 422


def test_get_addresses_empty():
    response = client.get("/addresses/")
    assert response.status_code == 404
    assert response.json() == {"detail": "No addresses found"}

def test_create_address_valid():
    data = {
        "address_1": "123 Main St",
        "city": "City",
        "state": "State",
        "zip": "12345",
        "country": "Country"
    }
    response = client.post("/addresses/", json=data)
    assert response.status_code == 422

def test_create_address_invalid():
    data = {
        "address_1": "",
        "city": "City",
        "state": "State",
        "zip": "12345",
        "country": "Country"
    }
    response = client.post("/addresses/", json=data)
    assert response.status_code == 422
