from pydantic import BaseModel

class BookingCreate(BaseModel):
    user_id: int
    event: str
    date: str
