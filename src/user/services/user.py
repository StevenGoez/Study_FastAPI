import re
from fastapi import HTTPException
from typing import List

from src.address.services.address import get_next_address_id
from src.databaseSimulation.databases import users_db
from src.user.models.user import User, UserCreate

user_id_counter = 0


def get_user() -> List[User]:
    if not users_db:
        raise HTTPException(status_code=404, detail="No users found")
    return users_db

def create_user(user_create: UserCreate) -> User:
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

# Función para obtener el próximo user_id y address_id
def get_next_user_id():
    global user_id_counter
    user_id_counter += 1
    return user_id_counter

# Función para validar el formato del correo electrónico
def valid_email(email):
    return "@" in email and (".com" in email or ".org" in email)

# Función para buscar un usuario por correo electrónico
def get_user_by_email(email):
    for user in users_db:
        if user.email == email:
            print(user.email)
            print(email)
            return user
    return None

# Función para buscar un usuario por user_id
def get_user_by_user_id(user_id):
    return next((user for user in users_db if user.user_id == user_id), None)
#
# Funcion para validar el password
def is_valid_password(password):
    uppercase_letter = re.search(r'[A-Z]', password)
    lowercase_letter = re.search(r'[a-z]', password)
    special_character = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    digit = re.search(r'\d', password)

    if uppercase_letter and lowercase_letter and special_character and digit:
        return True
    else:
        return False

def get_users_by_country(country: str) -> List[User]:
    # Filtrar usuarios por país
    filtered_users = [user for user in users_db if any(address.country == country for address in user.addresses)]

    if not filtered_users:
        raise HTTPException(status_code=404, detail=f"No users found for country: {country}")

    return filtered_users

