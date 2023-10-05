
from fastapi import HTTPException, APIRouter
from src.address.models.address import Address
from src.address.services.address import  create_address
from src.user.services.user import get_user_by_email

addressRouter=APIRouter()


# Ruta para crear una nueva dirección
@addressRouter.post("/addresses/", response_model=Address)
async def create_address_route(email: str, address_create: Address):
    user = get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=404, detail="User with provided email does not exist")

    address = create_address(user, address_create)

#     return address
# # Ruta para crear una nueva dirección
# @addressRouter.post("/addresses/", response_model=Address)
# async def create_address(email: str, address_create: Address):
#     # Validar que los campos obligatorios no estén vacíos ni tengan valores genéricos
#     if (
#         not address_create.address_1.strip() or
#         not address_create.city.strip() or
#         not address_create.state.strip() or
#         not address_create.zip.strip() or
#         not address_create.country.strip() or
#         address_create.address_1.lower() == "string" or
#         address_create.city.lower() == "string" or
#         address_create.state.lower() == "string" or
#         address_create.zip.lower() == "string" or
#         address_create.country.lower() == "string"
#     ):
#         raise HTTPException(status_code=400, detail="Please provide valid data")
#
#     # Validar el formato del correo electrónico
#     if not valid_email(email):
#         raise HTTPException(status_code=400, detail="Provide a valid email (e.g., example@domain.com or example@domain.org)")
#
    # # Verificar si el correo electrónico proporcionado corresponde a un usuario existente
    # user = get_user_by_email(email)
    # if user is None:
    #     raise HTTPException(status_code=404, detail="User with provided email does not exist")
#
#     # Obtener el próximo address_id
#     next_address_id = get_next_address_id()
#
#     # Crear una instancia de Address con address_id autogenerado
#     address = Address(
#         address_id=next_address_id,
#         address_1=address_create.address_1,
#         address_2=address_create.address_2,
#         city=address_create.city,
#         state=address_create.state,
#         zip=address_create.zip,
#         country=address_create.country
#     )
#
#     # Agregar la dirección a la lista
#     addresses_db.append(address)
#
#     # Asociar la dirección al usuario
#     user.addresses.append(address)
#
#     return address
#
#
# # Ruta para obtener todas las direcciones
# @addressRouter.get("/addresses/", response_model=List[Address])
# async def get_addresses():
#     return addresses_db

