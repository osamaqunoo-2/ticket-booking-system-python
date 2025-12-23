import requests
import time
import json
import psutil
import os

class GraphQLPerformanceTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.results = []

    def send_graphql(self, label, query_body):
        start = time.time()
        process = psutil.Process(os.getpid())
        try:
            response = requests.post(self.base_url, json={"query": query_body}, timeout=10)
        except Exception as e:
            print(f"❌ Error during {label}: {e}")
            self.results.append({
                "label": label,
                "status": 0,
                "time": 0,
                "sent": 0,
                "received": 0,
                "success": False
            })
            return None

        end = time.time()

        time_taken = round(end - start, 3)
        payload_sent = len(json.dumps({"query": query_body}).encode('utf-8'))
        payload_received = len(response.content)
        success = 200 <= response.status_code < 300

        print(f"{label}: {response.status_code} | Time: {time_taken}s | Sent: {payload_sent} B | Received: {payload_received} B")
        self.results.append({
            "label": label,
            "status": response.status_code,
            "time": time_taken,
            "sent": payload_sent,
            "received": payload_received,
            "success": success
        })

        return response

    def register_user(self):
        query = """
        mutation {
          registerUser(email: "test@example.com", username: "tester", password: "123456")
        }
        """
        return self.send_graphql("Register", query)

    def login_user(self):
        query = """
        mutation {
          loginUser(email: "test@example.com", password: "123456")
        }
        """
        return self.send_graphql("Login", query)

    def create_booking(self):
        query = """
        mutation {
          createBooking(booking: {
            userId: 1,
            event: "GraphQL Test Event",
            date: "2025-06-01"
          })
        }
        """
        return self.send_graphql("Booking", query)

    def create_payment(self):
        query = """
        mutation {
          createPayment(payment: {
            userId: 1,
            bookingId: 1,
            amount: 150.0,
            method: "credit_card",
            status: "paid"
          })
        }
        """
        return self.send_graphql("Payment", query)

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

        print("\n📊 GraphQL Performance Summary:")
        print(f"Total Requests: {total_requests}")
        print(f"✔️ Success Rate: {round((total_success / total_requests) * 100, 1)}%")
        print(f"❌ Error Rate: {round((total_failures / total_requests) * 100, 1)}%")
        print(f"⏱️ Avg Response Time: {avg_response}s | Max: {max_response}s | Min: {min_response}s")
        print(f"📤 Total Payload Sent: {total_sent / 1024:.2f} KB")
        print(f"📥 Total Payload Received: {total_received / 1024:.2f} KB")
        print(f"🚀 Throughput (RPS): {rps} requests/sec")
        print(f"🧠 Memory Before: {mem_before / 1024 / 1024:.2f} MB | After: {mem_after / 1024 / 1024:.2f} MB")
        print(f"⚙️ CPU Usage Before: {cpu_before}% | After: {cpu_after}%")

    def run_test(self):
        process = psutil.Process(os.getpid())
        cpu_before = psutil.cpu_percent(interval=1)
        mem_before = process.memory_info().rss
        start = time.time()

        self.register_user()
        self.login_user()
        self.create_booking()
        self.create_payment()

        end = time.time()
        cpu_after = psutil.cpu_percent(interval=1)
        mem_after = process.memory_info().rss

        self.print_summary(start, end, cpu_before, cpu_after, mem_before, mem_after)


if __name__ == "__main__":
    tester = GraphQLPerformanceTester("http://localhost:8000/graphql")
    tester.run_test()
