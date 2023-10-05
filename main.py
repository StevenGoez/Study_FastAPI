
from fastapi import FastAPI
from src.address.controllers.address import addressRouter
from src.user.controllers.user import userRouter

app = FastAPI()
app.include_router(userRouter)
app.include_router(addressRouter)


























