from typing import List

from fastapi import APIRouter, HTTPException, Query

#from src.address.services.address import get_next_address_id
from src.databaseSimulation.databases import users_db
from src.user.models.user import User, UserCreate
from src.user.services.user import get_next_user_id, valid_email, validate_user_create, associate_address_ids

userRouter=APIRouter()

# Ruta para obtener todos los usuarios
@userRouter.get("/users/", response_model=List[User])
async def get_users():
    if not users_db:
        raise HTTPException(status_code=404, detail="No users found")
    return users_db

@userRouter.post("/users/", response_model=User)
async def create_user(user_create: UserCreate):
    validate_user_create(user_create)  # Llama a la función de validación

    next_user_id = get_next_user_id()
    associate_address_ids(user_create.addresses)  # Asocia IDs de direcciones

    user = User(
        user_id=next_user_id,
        first_name=user_create.first_name,
        last_name=user_create.last_name,
        email=user_create.email,
        addresses=user_create.addresses
    )

    users_db.append(user)

    return user

# Ruta para obtener usuarios filtrados por país
@userRouter.get("/users-by-country/", response_model=List[User])
async def get_users_by_country(country: str = Query(..., description="Filter users by country")):
    # Filtrar usuarios por país
    filtered_users = [user for user in users_db if any(address.country == country for address in user.addresses)]

    if not filtered_users:
        raise HTTPException(status_code=404, detail=f"No users found for country: {country}")

    return filtered_users