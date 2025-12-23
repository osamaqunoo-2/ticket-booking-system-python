import grpc
import time
import sys
import os
import psutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.grpc_services import user_pb2, user_pb2_grpc
from app.grpc_services import booking_pb2, booking_pb2_grpc
from app.grpc_services import payment_pb2, payment_pb2_grpc

class GrpcPerformanceTester:
    def __init__(self, host="localhost:50051"):
        self.channel = grpc.insecure_channel(host)
        self.user_stub = user_pb2_grpc.UserServiceStub(self.channel)
        self.booking_stub = booking_pb2_grpc.BookingServiceStub(self.channel)
        self.payment_stub = payment_pb2_grpc.PaymentServiceStub(self.channel)
        self.results = []

    def measure(self, func, label):
        print(f"\n🔹 {label}")
        start = time.time()
        try:
            response = func()
            success = True
        except Exception as e:
            print(f"❌ Error: {e}")
            response = None
            success = False
        end = time.time()

        time_taken = round(end - start, 3)
        sent_size = 0  # gRPC ما بيعطي حجم المرسل بسهولة
        received_size = sys.getsizeof(response) if response else 0

        print(f"{label}: {'✔️' if success else '❌'} | Time: {time_taken}s | Received: {received_size} B")

        self.results.append({
            "label": label,
            "status": 200 if success else 0,
            "time": time_taken,
            "sent": sent_size,
            "received": received_size,
            "success": success
        })

        return response

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

    def print_summary(self, start_time, end_time, cpu_before, cpu_after, mem_before, mem_after):
        total_time = round(end_time - start_time, 3)
        total_sent = sum(r["sent"] for r in self.results)
        total_received = sum(r["received"] for r in self.results)
        total_requests = len(self.results)
        total_success = sum(1 for r in self.results if r["success"])
        total_failures = total_requests - total_success
        avg_response = round(sum(r["time"] for r in self.results) / total_requests, 3) if total_requests else 0
        max_response = max((r["time"] for r in self.results), default=0)
        min_response = min((r["time"] for r in self.results), default=0)
        rps = round(total_requests / total_time, 2) if total_time > 0 else "N/A"

        print("\n📊 gRPC Performance Summary:")
        print(f"Total Requests: {total_requests}")
        print(f"✔️ Success Rate: {round((total_success / total_requests) * 100, 1)}%")
        print(f"❌ Error Rate: {round((total_failures / total_requests) * 100, 1)}%")
        print(f"⏱️ Avg Response Time: {avg_response}s | Max: {max_response}s | Min: {min_response}s")
        print(f"📥 Total Payload Received: {total_received / 1024:.2f} KB")
        print(f"🚀 Throughput (RPS): {rps} requests/sec")
        print(f"🧠 Memory Before: {mem_before / 1024 / 1024:.2f} MB | After: {mem_after / 1024 / 1024:.2f} MB")
        print(f"⚙️ CPU Usage Before: {cpu_before}% | After: {cpu_after}%")

    def run_test(self):
        process = psutil.Process(os.getpid())
        cpu_before = psutil.cpu_percent(interval=1)
        mem_before = process.memory_info().rss
        start = time.time()

        reg = self.measure(self.register_user, "Register User")
        login = self.measure(self.login_user, "Login User")
        user_id = 1
        booking = self.measure(lambda: self.create_booking(user_id), "Create Booking")
        payment = self.measure(lambda: self.create_payment(user_id, booking_id=1), "Create Payment")

        end = time.time()
        cpu_after = psutil.cpu_percent(interval=1)
        mem_after = process.memory_info().rss

        self.print_summary(start, end, cpu_before, cpu_after, mem_before, mem_after)

if __name__ == "__main__":
    tester = GrpcPerformanceTester()
    tester.run_test()
