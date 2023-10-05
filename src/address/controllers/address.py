from typing import List

from fastapi import APIRouter, HTTPException

from src.address.models.address import Address, AddressCreate
from src.address.services.address import get_next_address_id
from src.databaseSimulation.databases import addresses_db
from src.user.services.user import get_user_by_email

addressRouter=APIRouter()


# Ruta para obtener todas las direcciones
@addressRouter.get("/addresses/", response_model=List[Address])
async def get_addresses():
    return addresses_db

@addressRouter.post("/addresses/", response_model=Address)
async def create_address(email: str, address_create: Address):
    validate_address_create(address_create)  # Llama a la función de validación

    user = get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User with provided email does not exist")

    next_address_id = get_next_address_id()
    address = create_address_instance(address_create, next_address_id)

    addresses_db.append(address)
    user.addresses.append(address)

    return address


def validate_address_create(address_create: Address):
    if (
        not address_create.address_1.strip() or
        not address_create.city.strip() or
        not address_create.state.strip() or
        not address_create.zip.strip() or
        not address_create.country.strip() or
        address_create.address_1.lower() == "string" or
        address_create.city.lower() == "string" or
        address_create.state.lower() == "string" or
        address_create.zip.lower() == "string" or
        address_create.country.lower() == "string"
    ):
        raise HTTPException(status_code=400, detail="Please provide valid data")

def create_address_instance(address_create: Address, address_id: int):
    return Address(
        address_id=address_id,
        address_1=address_create.address_1,
        address_2=address_create.address_2,
        city=address_create.city,
        state=address_create.state,
        zip=address_create.zip,
        country=address_create.country
    )





