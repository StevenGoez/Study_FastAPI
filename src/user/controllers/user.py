from typing import List
from fastapi import HTTPException, Query, APIRouter
from src.address.services.address import get_next_address_id
from src.databaseSimulation.databases import users_db
from src.user.models.user import User, UserCreate
from src.user.services.user import is_valid_password, get_next_user_id, valid_email

userRouter=APIRouter()



# Ruta para crear un nuevo usuario con direcciones
@userRouter.post("/users/", response_model=User)
async def create_user(user_create: UserCreate):
    # Verificar si el correo electrónico ya está en uso
    if any(u.email == user_create.email for u in users_db):
        raise HTTPException(status_code=400, detail="Email already registered")

    # Validar que los campos obligatorios no estén vacíos ni tengan valores genéricos
    if (
        not user_create.first_name.strip() or
        not user_create.last_name.strip() or
        not user_create.email.strip() or
        not user_create.password.strip() or
        user_create.first_name == "string" or
        user_create.last_name == "string" or
        user_create.email == "string"
    ):
        raise HTTPException(status_code=400, detail="Please provide valid data")

    # Validar el formato del correo electrónico
    if not valid_email(user_create.email):
        raise HTTPException(status_code=400, detail="Provide a valid email (e.g., example@domain.com or example@domain.org)")

        # Validar la contraseña
    if not is_valid_password(user_create.password):
        raise HTTPException(status_code=400,
                            detail="Password must contain at least one uppercase letter, one lowercase letter, and one special character")

    # Obtener el próximo user_id
    next_user_id = get_next_user_id()

    # Asociar el user_id a las direcciones
    for address in user_create.addresses:
        address.address_id = get_next_address_id()

    # Crear una instancia de User con user_id autogenerado y las direcciones
    user = User(
        user_id=next_user_id,
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        email=user_create.email,
        addresses=user_create.addresses
    )

    # Agregar el usuario a la lista
    users_db.append(user)

    return user

# Ruta para obtener todos los usuarios
@userRouter.get("/users/", response_model=List[User])
async def get_users():
    if not users_db:
        raise HTTPException(status_code=404, detail="No users found")
    return users_db


# Ruta para obtener usuarios filtrados por país
@userRouter.get("/users-by-country/", response_model=List[User])
async def get_users_by_country(country: str = Query(..., description="Filter users by country")):
    # Filtrar usuarios por país
    filtered_users = [user for user in users_db if any(address.country == country for address in user.addresses)]

    if not filtered_users:
        raise HTTPException(status_code=404, detail=f"No users found for country: {country}")

    return filtered_users
