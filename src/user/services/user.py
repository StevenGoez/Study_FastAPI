import re
import uuid
from fastapi import HTTPException
from src.databaseSimulation.databases import users_db
from src.user.models.user import UserCreate

def get_next_id():
    return uuid.uuid4()

# Función para validar el formato del correo electrónico
def valid_email(email):
    return "@" in email and (".com" in email or ".org" in email)

# Función para buscar un usuario por correo electrónico
def get_user_by_email(email):
    for user in users_db:
        if user.email == email:
            return user
    return None

# Función para buscar un usuario por user_id
def get_user_by_user_id(user_id):
    for user in users_db:
        if user.user_id == user_id:
            return user
    return None

def validate_user_create(user_create: UserCreate):
    if any(u.email == user_create.email for u in users_db):
        raise HTTPException(status_code=400, detail="Email already registered")

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

    if not valid_email(user_create.email):
        raise HTTPException(status_code=400, detail="Provide a valid email (e.g., example@domain.com or example@domain.org)")

def associate_address_ids(addresses):
    for idx, address in enumerate(addresses):
        address[idx] = get_next_id()

def is_valid_password(password):
    pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@/#$%^&*()_+{}|:"<>?~]).*$'
    return bool(re.match(pattern, password))



