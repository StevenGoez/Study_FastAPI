from unittest.mock import MagicMock
import pytest
from starlette.testclient import TestClient
from main import app
from src.user.controllers.user import create_user, get_users, get_users_by_country
from src.user.models.user import UserCreate, User

client = TestClient(app)


@pytest.mark.asyncio
async def test_create_user():
    # Configurar datos de prueba
    user_create = UserCreate(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        password="P@ssw0rd",
    )

    user = await create_user(user_create)  # Esperar a que se complete la coroutine
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john@example.com"

def test_get_users_empty():
    response = client.get("/users/")
    assert response.status_code == 404
    assert response.json() == {"detail": "No users found"}

@pytest.mark.asyncio
async def test_get_users_by_country():
    # Mockear dependencias externas como se necesite (por ejemplo, la base de datos)
    users_mock = [
        User(user_id="1", first_name="Alejo", last_name="Velez", email="alejo@example.com", addresses=["US"]),
        User(user_id="2", first_name="Bob", last_name="Monroy", email="bob@example.com", addresses=["CA"]),
        User(user_id="3", first_name="Sara", last_name="Ramirez", email="sara@example.com", addresses=["US"]),
    ]

    # Simular la obtención de usuarios de la base de datos
    get_users_by_country_mock = MagicMock(return_value=users_mock)

    country = "US"
    users = await get_users_by_country(country, get_users_by_country_mock)
    assert len(users) == 2
    assert users[0].first_name == "Alejo"
    assert users[1].first_name == "Sara"


def test_get_users_by_country_invalid():
    # Intentar obtener usuarios en un país que no existe en las direcciones
    response = client.get("/users-by-country/?country=Canada")
    assert response.status_code == 404
    assert response.json() == {"detail": "No users found for country: Canada"}

@pytest.mark.asyncio
async def test_get_users():
    # Mockear dependencias externas como se necesite (por ejemplo, la base de datos)
    users_mock = [
        User(user_id="1", first_name="Laura", last_name="Goez", email="laurae@example.com"),
        User(user_id="2", first_name="Bob", last_name="Bedoya", email="bob@example.com"),
    ]

    # Simular la obtención de usuarios de la base de datos
    get_users_mock = MagicMock(return_value=users_mock)

    # Prueba exitosa
    users = await get_users(get_users_mock)
    assert len(users) == 2
    assert users[0].first_name == "Laura"
    assert users[1].first_name == "Bob"