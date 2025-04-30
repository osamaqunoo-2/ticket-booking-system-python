from fastapi import FastAPI
from app.api import user
from app.core.database import Base, engine

from fastapi.middleware.cors import CORSMiddleware

import time

from app.models import user_model
app = FastAPI()

#app.include_router(user.router)
app.include_router(user.router, prefix="/users", tags=["Users"])
time.sleep(5)

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # أثناء التطوير ممكن نخليها مفتوحة
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"message": "Welcome to Ticket Booking System API!123"}

#start server
#uvicorn app.main:app --reload


#on brawser
#http://127.0.0.1:8000/users

#python -m uvicorn app.main:app --reload


#لو بدنا نغير على الداتا بيز لازم نمسحها docker-compose down --volumes
#docker-compose up --build


#python healthcheck.py
