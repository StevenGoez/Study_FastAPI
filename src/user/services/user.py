import re
from src.databaseSimulation.databases import users_db

user_id_counter = 0

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
            return user
    return None

# Función para buscar un usuario por user_id
def get_user_by_user_id(user_id):
    for user in users_db:
        if user.user_id == user_id:
            return user
    return None


