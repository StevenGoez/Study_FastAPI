from unittest.mock import Mock
import pytest
from fastapi import HTTPException
from src.databaseSimulation.databases import users_db
from src.user.models.user import UserCreate
from src.user.services.user import get_next_id, valid_email, get_user_by_email, validate_user_create, is_valid_password

def test_get_next_id():
    # Prueba la generación de IDs únicos
    id_1 = get_next_id()
    id_2 = get_next_id()
    assert id_1 != id_2

def test_valid_email():
    # Prueba la validación de correos electrónicos
    assert valid_email("test@example.com")
    assert valid_email("test@example.org")
    assert not valid_email("invalid_email")
    assert not valid_email("test@example")

def test_get_user_by_email():
    # Configurar datos de prueba
    user_mock = Mock()
    user_mock.email = "test@example.com"
    users_db.append(user_mock)  # Agregar el usuario mock a la lista mock de users_db

    # Prueba la búsqueda exitosa
    user = get_user_by_email("test@example.com")
    assert user == user_mock
def test_validate_user_create():
    # Prueba la validación exitosa
    user_create = UserCreate(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        password="P@ssw0rd",
    )
    validate_user_create(user_create)

    # Prueba cuando falta el campo email
    user_create.email = ""
    with pytest.raises(HTTPException):
        validate_user_create(user_create)

    # Prueba cuando el email es inválido
    user_create.email = "invalid_email"
    with pytest.raises(HTTPException):
        validate_user_create(user_create)

def test_is_valid_password():
    # Prueba la validación de contraseñas
    assert is_valid_password("P@ssw0rd")
    assert not is_valid_password("password123")
    assert not is_valid_password("P@ssw")
    assert not is_valid_password("12345678")
    assert not is_valid_password("!@#$%^&*()_")