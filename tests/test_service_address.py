import uuid
from fastapi import HTTPException
from src.address.models.address import AddressCreate, Address
from src.address.services.address import  create_address_instance

def test_validate_address_create():
    # Prueba la validación de direcciones
    address_create = AddressCreate(
        address_1="123 Main St",
        address_2="Apt 101",
        city="City",
        state="State",
        zip="12345",
        country="Country",
        email="test@example.com"
    )

def test_create_address_instance_with_invalid_data():
    invalid_address_data = {
        "address_1": "",
        "address_2": "",
        "city": "City",
        "state": "State",
        "zip": "12345",
        "country": "Country",
        "email": ""
    }

    address_id = 1
    try:
        create_address_instance(AddressCreate(**invalid_address_data), address_id)
    except HTTPException as exc:
        assert exc.status_code == 400
        assert exc.detail == "address_1 cannot be empty"
    else:
        assert False, "Expected HTTPException was not raised"

def test_create_address_instance():
    # Prueba la creación de una instancia de dirección válida
    address_create = AddressCreate(
        address_1="123 Main St",
        address_2="Apt 4B",  # Agregar un valor para address_2
        city="City",
        state="State",
        zip="12345",
        country="Country",
        email="test@example.com"
    )
    address_id = uuid.uuid4()  # Genera un UUID aleatorio
    address_instance = create_address_instance(address_create, address_id)
    assert isinstance(address_instance, Address)
    assert address_instance.address_id == address_id
    assert address_instance.address_1 == "123 Main St"
    assert address_instance.address_2 == "Apt 4B"  # Verificar que address_2 se haya configurado correctamente
    assert address_instance.city == "City"
    assert address_instance.state == "State"
    assert address_instance.zip == "12345"
    assert address_instance.country == "Country"