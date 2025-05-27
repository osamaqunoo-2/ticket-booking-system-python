import grpc
import time
import sys
import os
import psutil
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.grpc_services import payment_pb2, payment_pb2_grpc

class GrpcLoadTester:
    def __init__(self, host="localhost:50051"):
        self.channel = grpc.insecure_channel(host)
        self.stub = payment_pb2_grpc.PaymentServiceStub(self.channel)
        self.results = []

    def send_payment(self, i):
        start = time.time()
        try:
            response = self.stub.CreatePayment(payment_pb2.PaymentRequest(
                user_id=1,
                booking_id=random.randint(1, 10000),
                amount=150.0,
                method="credit_card",
                status="paid"
            ))
            success = response.success
        except Exception:
            response = None
            success = False
        end = time.time()

        time_taken = round(end - start, 3)
        received_size = sys.getsizeof(response) if response else 0

        self.results.append({
            "status": 200 if success else 0,
            "time": time_taken,
            "received": received_size,
            "success": success
        })

    def run_test(self, user_count=1000):
        process = psutil.Process(os.getpid())
        cpu_before = psutil.cpu_percent(interval=1)
        mem_before = process.memory_info().rss
        start = time.time()

        with ThreadPoolExecutor(max_workers=200) as executor:
            futures = [executor.submit(self.send_payment, i) for i in range(user_count)]
            for future in as_completed(futures):
                future.result()

        end = time.time()
        cpu_after = psutil.cpu_percent(interval=1)
        mem_after = process.memory_info().rss

        self.print_summary(start, end, cpu_before, cpu_after, mem_before, mem_after)

    def print_summary(self, start_time, end_time, cpu_before, cpu_after, mem_before, mem_after):
        total_time = round(end_time - start_time, 3)
        total_received = sum(r["received"] for r in self.results)
        total_requests = len(self.results)
        total_success = sum(1 for r in self.results if r["success"])
        total_failures = total_requests - total_success
        avg_response = round(sum(r["time"] for r in self.results) / total_requests, 3) if total_requests else 0
        max_response = max((r["time"] for r in self.results), default=0)
        min_response = min((r["time"] for r in self.results), default=0)
        rps = round(total_requests / total_time, 2) if total_time > 0 else "N/A"

        print("\n📊 gRPC Load Test Summary (1000 Users):")
        print(f"Total Requests: {total_requests}")
        print(f"✔️ Success Rate: {round((total_success / total_requests) * 100, 1)}%")
        print(f"❌ Error Rate: {round((total_failures / total_requests) * 100, 1)}%")
        print(f"⏱️ Avg Response Time: {avg_response}s | Max: {max_response}s | Min: {min_response}s")
        print(f"📥 Total Payload Received: {total_received / 1024:.2f} KB")
        print(f"🚀 Throughput (RPS): {rps} requests/sec")
        print(f"🧠 Memory Before: {mem_before / 1024 / 1024:.2f} MB | After: {mem_after / 1024 / 1024:.2f} MB")
        print(f"⚙️ CPU Usage Before: {cpu_before}% | After: {cpu_after}%")

if __name__ == "__main__":
    tester = GrpcLoadTester()
    tester.run_test(user_count=1000)
