from typing import List
from fastapi import APIRouter, HTTPException
from src.address.models.address import Address, AddressCreate
from src.address.services.address import create_address_instance, validate_address_create
from src.databaseSimulation.databases import addresses_db
from src.user.services.user import get_user_by_email, get_next_id

addressRouter=APIRouter()


# Ruta para obtener todas las direcciones
@addressRouter.get("/addresses/", response_model=List[Address])
async def get_addresses():
    if not addresses_db:
        raise HTTPException(status_code=404, detail="No addresses found")
    return addresses_db

@addressRouter.post("/addresses/", response_model=Address)
async def create_address(email: str, address_create: Address):
    validate_address_create(address_create)  # Llama a la función de validación

    user = get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User with provided email does not exist")

    next_address_id = get_next_id()
    address = create_address_instance(address_create, next_address_id)

    addresses_db.append(address)
    user.addresses.append(address)

    return address






