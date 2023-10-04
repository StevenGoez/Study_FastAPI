from ...address.models.address import Address
from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    addresses: List[Address] = []

class User(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: str
    addresses: List[Address] = []