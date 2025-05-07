import strawberry
from typing import List
from app.models.booking_model import Booking as BookingModel
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.core.database import SessionLocal


@strawberry.type
class BookingType:
    id: int
    user_id: int
    event: str
    date: str


@strawberry.type
class BookingQuery:
    @strawberry.field
    def all_bookings(self) -> List[BookingType]:
        db = SessionLocal()
        try:
            bookings = db.query(BookingModel).all()
            return [BookingType(**b.__dict__) for b in bookings]
        finally:
            db.close()

@strawberry.type
class BookingMutation:
    @strawberry.mutation
    def create_booking(self, user_id: int, event: str, date: str) -> BookingType:
        db: Session = next(get_db())
        booking = BookingModel(user_id=user_id, event=event, date=date)
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return BookingType(**booking.__dict__)
