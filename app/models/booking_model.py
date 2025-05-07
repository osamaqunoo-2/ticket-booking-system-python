from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    event = Column(String, nullable=False)
    date = Column(String, nullable=False)
