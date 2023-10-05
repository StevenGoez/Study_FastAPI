from fastapi import HTTPException
from typing import Optional
from src.address.models.address import Address
from src.databaseSimulation.databases import addresses_db
from src.user.controllers import user
from src.user.models.user import User

address_id_counter = 0
def valid_email(email: str) -> bool:
    if not valid_email(email):
        raise HTTPException(status_code=400, detail="Provide a valid email (e.g., example@domain.com or example@domain.org)")

def get_user_by_email(email: str) -> Optional[User]:
    if user is None:
        raise HTTPException(status_code=404, detail="User with provided email does not exist")

def create_address(user: User, address_data: Address) -> Address:
    # Validar que los campos obligatorios no estén vacíos ni tengan valores genéricos
    if (
        not address_data.address_1.strip() or
        not address_data.city.strip() or
        not address_data.state.strip() or
        not address_data.zip.strip() or
        not address_data.country.strip() or
        address_data.address_1.lower() == "string" or
        address_data.city.lower() == "string" or
        address_data.state.lower() == "string" or
        address_data.zip.lower() == "string" or
        address_data.country.lower() == "string"
    ):
        raise ValueError("Please provide valid data")

    # Crear una instancia de Address con address_id autogenerado
    next_address_id = get_next_address_id()
    address = Address(
        address_id=next_address_id,
        address_1=address_data.address_1,
        address_2=address_data.address_2,
        city=address_data.city,
        state=address_data.state,
        zip=address_data.zip,
        country=address_data.country
    )

    # Agregar la dirección a la lista (simulando una base de datos)
    addresses_db.append(address)

    # Asociar la dirección al usuario
    user.addresses.append(address)

    return address

# Función para obtener el próximo address_id
def get_next_address_id():
    global address_id_counter
    address_id_counter += 1
    return address_id_counter
