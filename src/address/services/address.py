from fastapi import HTTPException
from src.address.models.address import Address

address_id_counter = 0

# Función para obtener el próximo address_id
def get_next_address_id():
    global address_id_counter
    address_id_counter += 1
    return address_id_counter

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
    if not address_create.address_1.strip():
        raise HTTPException(status_code=400, detail="address_1 cannot be empty")

    return Address(
        address_id=address_id,
        address_1=address_create.address_1,
        address_2=address_create.address_2,
        city=address_create.city,
        state=address_create.state,
        zip=address_create.zip,
        country=address_create.country
    )
