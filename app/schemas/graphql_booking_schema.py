import strawberry
from app.models.booking_model import Booking as BookingModel
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from typing import List

# النوع المستخدم في الإرجاع
@strawberry.type
class BookingType:
    id: int
    user_id: int
    event: str
    date: str

# الإدخال لإنشاء الحجز
@strawberry.input
class BookingInput:
    user_id: int
    event: str
    date: str

# الإدخال لتحديث الحجز (يحتوي على ID)
@strawberry.input
class BookingUpdateInput:
    id: int
    user_id: int
    event: str
    date: str

# استعلامات الحجز
@strawberry.type
class BookingQuery:
    @strawberry.field
    def all_bookings(self) -> List[BookingType]:
        db: Session = SessionLocal()
        try:
            bookings = db.query(BookingModel).all()
            return [BookingType(**b.__dict__) for b in bookings]
        finally:
            db.close()

# التعديلات (mutation)
@strawberry.type
class BookingMutation:
    @strawberry.mutation
    def create_booking(self, booking: BookingInput) -> str:
        db: Session = SessionLocal()
        try:
            new_booking = BookingModel(**booking.__dict__)
            db.add(new_booking)
            db.commit()
            return f"✅ Booking created with ID {new_booking.id}"
        except Exception as e:
            return f"❌ Error: {str(e)}"
        finally:
            db.close()

    @strawberry.mutation
    def update_booking(self, booking: BookingUpdateInput) -> str:
        db: Session = SessionLocal()
        try:
            existing = db.query(BookingModel).filter(BookingModel.id == booking.id).first()
            if not existing:
                return f"❌ Booking with ID {booking.id} not found"
            existing.user_id = booking.user_id
            existing.event = booking.event
            existing.date = booking.date
            db.commit()
            return f"✅ Booking ID {booking.id} updated successfully"
        except Exception as e:
            return f"❌ Error updating: {str(e)}"
        finally:
            db.close()

    @strawberry.mutation
    def delete_booking(self, booking_id: int) -> str:
        db: Session = SessionLocal()
        try:
            booking = db.query(BookingModel).filter(BookingModel.id == booking_id).first()
            if not booking:
                return f"❌ Booking with ID {booking_id} not found"
            db.delete(booking)
            db.commit()
            return f"🗑️ Booking ID {booking_id} deleted"
        except Exception as e:
            return f"❌ Error deleting: {str(e)}"
        finally:
            db.close()
