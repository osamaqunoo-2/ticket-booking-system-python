from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ✅ ربط المفتاح الخارجي
    event = Column(String, nullable=False)
    date = Column(String, nullable=False)

    user = relationship("User", back_populates="bookings")  # ✅ العلاقة العكسية
