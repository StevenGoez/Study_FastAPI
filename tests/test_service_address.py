import pytest
from fastapi import HTTPException

from src.address.models.address import Address
from src.address.services.address import validate_address_create, create_address_instance

# Datos de prueba

valid_address_data = {
    "address_id": 1,
    "address_1": "123 Main St",
    "address_2": "optional_address_2",
    "city": "New York",
    "state": "NY",
    "zip": "10001",
    "country": "USA"
}

invalid_address_data = {
    "address_id": 1,
    "address_1": "string",
    "address_2": "optional_address_2",
    "city": "New York",
    "state": "",
    "zip": "10001",
    "country": "USA"
}


def test_validate_address_create_valid():
    address = Address(**valid_address_data)
    assert validate_address_create(address) is None


def test_validate_address_create_invalid():
    invalid_address = Address(**invalid_address_data)
    with pytest.raises(HTTPException) as exc_info:
        validate_address_create(invalid_address)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Please provide valid data"


def test_create_address_instance():
    address_create = Address(**valid_address_data)
    address_id = 1
    address_instance = create_address_instance(address_create, address_id)

    assert address_instance.address_id == address_id
    assert address_instance.address_1 == address_create.address_1
    assert address_instance.city == address_create.city
    assert address_instance.state == address_create.state
    assert address_instance.zip == address_create.zip
    assert address_instance.country == address_create.country

@pytest.mark.xfail
def test_create_address_instance_with_invalid_data():
    invalid_address_create = Address(**invalid_address_data)
    address_id = 1
    try:
        create_address_instance(invalid_address_create, address_id)
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "address_1 cannot be empty"
    else:
        assert False, "Expected HTTPException was not raised"