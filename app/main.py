from fastapi import FastAPI
from app.api import user

app = FastAPI()

app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Welcome to Ticket Booking System API!123"}

#start server
#uvicorn app.main:app --reload


#on brawser
#http://127.0.0.1:8000/users

#python -m uvicorn app.main:app --reload


