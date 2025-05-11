import grpc
from app.grpc_services import user_pb2, user_pb2_grpc
from app.grpc_services import booking_pb2, booking_pb2_grpc

def run():
    # الاتصال بالخادم gRPC
    channel = grpc.insecure_channel("localhost:50051")

    # Stub لخدمة المستخدمين
    user_stub = user_pb2_grpc.UserServiceStub(channel)

    print("\n📤 Trying to register...")
    register_response = user_stub.Register(user_pb2.RegisterRequest(
        email="osamad@gmail.com",
        username="osama",
        password="123456"
    ))
    print("✅ Register Response:", register_response.message)

    print("\n📤 Trying to login...")
    login_response = user_stub.Login(user_pb2.LoginRequest(
        email="osama@gmail.com",
        password="123456"
    ))
    print("✅ Login Response:", login_response.message)

    # Stub لخدمة الحجوزات
    booking_stub = booking_pb2_grpc.BookingServiceStub(channel)

    print("\n📤 Creating a booking...")
    booking_response = booking_stub.CreateBooking(booking_pb2.BookingRequest(
        user_id=1,
        event="AI Conference",
        date="2025-05-30"
    ))
    print("✅ Create Booking:", booking_response.message)

    print("\n📥 Getting all bookings...")
    bookings = booking_stub.GetAllBookings(booking_pb2.Empty())
    for b in bookings:
        print(f"📄 Booking ID: {b.id}, User: {b.user_id}, Event: {b.event}, Date: {b.date}")

    print("\n🗑️ Deleting booking with ID 1...")
    delete_response = booking_stub.DeleteBooking(booking_pb2.DeleteBookingRequest(
        booking_id=1
    ))
    print("✅ Delete Booking:", delete_response.message)

if __name__ == "__main__":
    run()
