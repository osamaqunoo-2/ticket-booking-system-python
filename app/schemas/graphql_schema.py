import strawberry
from app.core.database import SessionLocal
from app.models.user_model import User as UserModel
from app.schemas.user_schema import UserCreate, UserLogin
from passlib.hash import bcrypt
from app.models.booking_model import Booking as BookingModel
from typing import List
from sqlalchemy.orm import Session

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



@strawberry.type
class Mutation:
    @strawberry.mutation
    def all_bookings(self) -> List[BookingType]:
        db: Session = SessionLocal()
        try:
            bookings = db.query(BookingModel).all()
            return [BookingType(
                id=b.id,
                user_id=b.user_id,
                event=b.event,
                date=b.date
            ) for b in bookings]
        finally:
            db.close()
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


    @strawberry.mutation
    def register_user(self, email: str, username: str, password: str) -> str:
        try:
            user_data = UserCreate(email=email, username=username, password=password)
        except Exception as e:
            return f"❌ Invalid data: {str(e)}"

        db = SessionLocal()
        try:
            if db.query(UserModel).filter(UserModel.email == user_data.email).first():
                return "❌ Email already registered"

            new_user = UserModel(
                email=user_data.email,
                username=user_data.username,
                password=user_data.password  # استخدم bcrypt.hash(user_data.password) لو بدك تشفير
            )
            db.add(new_user)
            db.commit()
            return "✅ User registered successfully"
        finally:
            db.close()

    @strawberry.mutation
    def login_user(self, email: str, password: str) -> str:
        try:
            login_data = UserLogin(email=email, password=password)
        except Exception as e:
            return f"❌ Invalid input: {str(e)}"

        db = SessionLocal()
        try:
            db_user = db.query(UserModel).filter(UserModel.email == login_data.email).first()
            if not db_user:
                return "❌ Invalid email"

            if db_user.password != login_data.password:
                return "❌ Incorrect password"

            return "✅ Login successful"
        finally:
            db.close()


@strawberry.type
class Query:
    hello: str = "GraphQL is connected to database!"

schema = strawberry.Schema(query=Query, mutation=Mutation)
