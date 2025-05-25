import grpc
import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.grpc_services import user_pb2, user_pb2_grpc
from app.grpc_services import booking_pb2, booking_pb2_grpc
from app.grpc_services import payment_pb2, payment_pb2_grpc

class GrpcPerformanceTester:
    print("🚀 Starting gRPC test...")

    def __init__(self, host="localhost:50051"):
        self.channel = grpc.insecure_channel(host)
        self.user_stub = user_pb2_grpc.UserServiceStub(self.channel)
        self.booking_stub = booking_pb2_grpc.BookingServiceStub(self.channel)
        self.payment_stub = payment_pb2_grpc.PaymentServiceStub(self.channel)

    def measure(self, func, label):
        print(f"\n🔹 {label}")
        start = time.time()
        result = func()
        end = time.time()
        print(f"⏱️ Took: {round((end - start)*1000, 2)} ms")
        return result

    def register_user(self):
        return self.user_stub.Register(user_pb2.RegisterRequest(
            email="test@example.com",
            username="tester",
            password="123456"
        ))

    def login_user(self):
        return self.user_stub.Login(user_pb2.LoginRequest(
            email="test@example.com",
            password="123456"
        ))

    def create_booking(self, user_id):
        return self.booking_stub.CreateBooking(booking_pb2.BookingRequest(
            user_id=user_id,
            event="AI Conference",
            date="2025-05-30"
        ))

    def create_payment(self, user_id, booking_id):
        return self.payment_stub.CreatePayment(payment_pb2.PaymentRequest(
            user_id=user_id,
            booking_id=booking_id,
            amount=150.0,
            method="credit_card",
            status="paid"
        ))

    def run_test(self):
        reg = self.measure(self.register_user, "Register User")
        print(reg.message)

        login = self.measure(self.login_user, "Login User")
        print(login.message)
       # if not login.success:
        #    return
        user_id = 1 #login.user_id

        booking = self.measure(lambda: self.create_booking(user_id), "Create Booking")
        print(booking.message)

        payment = self.measure(lambda: self.create_payment(user_id, booking_id=1), "Create Payment")
        print(payment.message)


if __name__ == "__main__":
    tester = GrpcPerformanceTester()
    tester.run_test()
