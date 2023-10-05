# Fixture de ejemplo para usuarios en users_db
import pytest
from fastapi import HTTPException

from src.user.models.user import UserCreate
from src.user.services.user import get_next_user_id, valid_email, get_user_by_email, validate_user_create, \
    associate_address_ids



@pytest.fixture
def example_users():
    return [
        UserCreate(first_name="John", last_name="Doe", email="johndoe@example.com", password="password"),
        UserCreate(first_name="Alice", last_name="Smith", email="alice@example.com", password="password"),
    ]



def test_get_next_user_id():
    assert get_next_user_id() == 1
    assert get_next_user_id() == 2

def test_valid_email():
    assert valid_email("example@example.com") is True
    assert valid_email("invalid-email") is False

@pytest.mark.xfail
def test_get_user_by_email(example_users):
    user = get_user_by_email("johndoe@example.com")
    assert user is not None
    assert user.first_name == "John"

    user = get_user_by_email("nonexistent@example.com")
    assert user is None


def test_validate_user_create(example_users):
    with pytest.raises(HTTPException) as exc_info:
        validate_user_create(UserCreate(first_name="string", last_name="Doe", email="johndoe@example.com", password="password"))
    assert exc_info.value.status_code == 400


def test_associate_address_ids():
    addresses = [{"address_id": 0}, {"address_id": 0}]
    associate_address_ids(addresses)
    assert addresses[0]["address_id"] == 1
    assert addresses[1]["address_id"] == 2