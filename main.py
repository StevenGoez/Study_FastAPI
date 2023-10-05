
from fastapi import FastAPI
from src.address.controllers.address import addressRouter
from src.user.controllers.user import userRouter

app = FastAPI()
app.include_router(userRouter)
app.include_router(addressRouter)

# @app.get("/")
# def welcome_page():
#     return{"Welcome": "welcome please change the URL to: http://127.0.0.1:8000/docs"}

























