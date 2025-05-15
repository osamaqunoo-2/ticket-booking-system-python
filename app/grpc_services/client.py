import grpc
from app.grpc_services import user_pb2, user_pb2_grpc
from app.grpc_services import booking_pb2, booking_pb2_grpc
from app.grpc_services import payment_pb2, payment_pb2_grpc  # ✅ استيراد الدفع

def run():
    # الاتصال بالخادم gRPC
    channel = grpc.insecure_channel("localhost:50051")

    # Stub لخدمة المستخدمين
    user_stub = user_pb2_grpc.UserServiceStub(channel)

    print("\n📤 Trying to register...")
    register_response = user_stub.Register(user_pb2.RegisterRequest(
        email="osama@gmail.com",
        username="osama",
        password="123456"
    ))
    if register_response.success:
        print("✅ Register Response:", register_response.message)
    else:
        print("❌ Register Failed:", register_response.message)

    print("\n📤 Trying to login...")
    login_response = user_stub.Login(user_pb2.LoginRequest(
        email="osama@gmail.com",
        password="123456"
    ))
    if login_response.success:
        print("✅ Login Response:", login_response.message)
        user_id = login_response.user_id
    else:
        print("❌ Login Failed:", login_response.message)
       # return

    # Stub لخدمة الحجوزات
    booking_stub = booking_pb2_grpc.BookingServiceStub(channel)

    print("\n📤 Creating a booking...")
    booking_response = booking_stub.CreateBooking(booking_pb2.BookingRequest(
        user_id=1,
        event="AI Conference",
        date="2025-05-30"
    ))
    if booking_response.success:
        print("✅ Booking Created:", booking_response.message)
    else:
        print("❌ Booking Failed:", booking_response.message)

    print("\n📥 Getting all bookings...")
   # try:
    #    bookings = booking_stub.GetAllBookings(booking_pb2.Empty())
     #   last_booking_id = None
      #  for b in bookings:
       #     print(f"📄 Booking ID: {b.id} | User: {b.user_id} | Event: {b.event} | Date: {b.date}")
        #    last_booking_id = b.id  # خذ آخر ID لاستخدامه في الدفع
    #except Exception as e:
     #   print("❌ Failed to get bookings:", e)
        #return

    # Stub لخدمة الدفع
    payment_stub = payment_pb2_grpc.PaymentServiceStub(channel)

    print("\n💳 Creating a payment...")
    payment_response = payment_stub.CreatePayment(payment_pb2.PaymentRequest(
        user_id=1,
        booking_id=1,
        amount=99.99,
        method="credit_card",
        status="success"
    ))
    if payment_response.success:
        print("✅ Payment Created:", payment_response.message)
    else:
        print("❌ Payment Failed:", payment_response.message)

    print("\n📥 Getting all payments...")
    try:
        payments = payment_stub.GetAllPayments(payment_pb2.Empty())
        for p in payments:
            print(f"💰 Payment ID: {p.id} | Booking: {p.booking_id} | Amount: {p.amount} | Method: {p.method} | Status: {p.status}")
    except Exception as e:
        print("❌ Failed to get payments:", e)

    print("\n🗑️ Deleting payment with ID 1...")
    delete_response = payment_stub.DeletePayment(payment_pb2.PaymentIdRequest(
        payment_id=1
    ))
    if delete_response.success:
        print("✅ Payment Deleted:", delete_response.message)
    else:
        print("❌ Payment Delete Failed:", delete_response.message)

if __name__ == "__main__":
    run()
