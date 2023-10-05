import pytest
from starlette.testclient import TestClient

from main import app

client = TestClient(app)  # Supongo que tienes una instancia de FastAPI llamada 'app'

def test_get_users_empty():
    response = client.get("/users/")
    assert response.status_code == 404
    assert response.json() == {"detail": "No users found"}


@pytest.mark.xfail
def test_create_user_valid():
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com",
        "addresses": [
            {
                "address_1": "123 Main St",
                "city": "City",
                "state": "State",
                "zip": "12345",
                "country": "USA"
            }
        ]
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200

@pytest.mark.xfail
def test_create_user_invalid():
    user_data = {
        "first_name": "string",
        "last_name": "Doe",
        "email": "johndoe@example.com",
        "addresses": []
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 400

@pytest.mark.xfail
def test_get_users_by_country_valid():
    # Agregar usuarios con direcciones en el mismo país (USA)
    user1_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com",
        "addresses": [
            {
                "address_1": "123 Main St",
                "city": "City",
                "state": "State",
                "zip": "12345",
                "country": "USA"
            }
        ]
    }
    user2_data = {
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice@example.com",
        "addresses": [
            {
                "address_1": "456 Elm St",
                "city": "City",
                "state": "State",
                "zip": "67890",
                "country": "USA"
            }
        ]
    }
    client.post("/users/", json=user1_data)
    client.post("/users/", json=user2_data)

    response = client.get("/users-by-country/?country=USA")
    assert response.status_code == 200  # Verifica que el código de estado sea 200
    users = response.json()
    assert len(users) == 2  # Verifica que se obtengan los dos usuarios


def test_get_users_by_country_invalid():
    # Intentar obtener usuarios en un país que no existe en las direcciones
    response = client.get("/users-by-country/?country=Canada")
    assert response.status_code == 404
    assert response.json() == {"detail": "No users found for country: Canada"}