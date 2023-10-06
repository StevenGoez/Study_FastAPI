from http import client
from unittest.mock import MagicMock
import pytest
from fastapi.testclient import TestClient
from main import app
from src.address.controllers.address import create_address, get_addresses
from src.address.models.address import AddressCreate

client = TestClient(app)

@pytest.mark.asyncio
async def test_create_address():
    # Configurar datos de prueba
    email = "john@example.com"
    address_create = AddressCreate(
        address_1="123 Main St",
        address_2="Apt 4B",
        city="City",
        state="State",
        zip="12345",
        country="Country",
        email=email,
    )

    # Mockear dependencias externas como se necesite (por ejemplo, la base de datos)
    user_mock = MagicMock()  # Simular un usuario existente
    get_user_by_email_mock = MagicMock(return_value=user_mock)

    address = await create_address(email, address_create, get_user_by_email_mock)
    assert address.address_1 == "123 Main St"
    assert address.address_2 == "Apt 4B"
    assert address.city == "City"
    assert address.state == "State"
    assert address.zip == "12345"
    assert address.country == "Country"
    assert address.email == email
def test_get_addresses_empty():
    response = client.get("/addresses/")
    assert response.status_code == 404
    assert response.json() == {"detail": "No addresses found"}

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

@pytest.mark.asyncio
async def test_get_addresses():
    # Mockear dependencias externas como se necesite (por ejemplo, la base de datos)
    addresses_db_mock = [MagicMock() for _ in range(3)]

    # Prueba exitosa
    addresses = await get_addresses(addresses_db_mock)
    assert len(addresses) == 3

@pytest.mark.asyncio
async def test_create_address_with_nonexistent_email():
    # Configurar datos de prueba
    email = "nonexistent@example.com"
    address_create = AddressCreate(
        address_1="123 Main St",
        city="City",
        state="State",
        zip="12345",
        country="Country",
        email=email,
    )