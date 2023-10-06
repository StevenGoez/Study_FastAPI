from uuid import UUID
from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    addresses: List[UUID] = []

class User(BaseModel):
    user_id: UUID
    first_name: str
    last_name: str
    email: str
    addresses: List[UUID] = []