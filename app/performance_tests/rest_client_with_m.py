import requests
import time
import json
import psutil
import os

BASE_URL = "http://localhost:8000"
email = "testuser@example.com"
password = "test123"
username = "testuser"

results = []

def measure_request(label, method, url, json_data=None):
    start = time.time()
    response = requests.request(method, url, json=json_data)
    end = time.time()

    time_taken = round(end - start, 3)
    payload_sent = len(json.dumps(json_data or {}).encode('utf-8'))
    payload_received = len(response.content)

    success = 200 <= response.status_code < 300
    results.append({
        "label": label,
        "status": response.status_code,
        "time": time_taken,
        "sent": payload_sent,
        "received": payload_received,
        "success": success
    })

    print(f"🔹 {label}: {response.status_code} | Time: {time_taken}s | Sent: {payload_sent} B | Received: {payload_received} B")
    return response

def register_user():
    return measure_request("Register", "POST", f"{BASE_URL}/users/register", {
        "email": email,
        "password": password,
        "username": username
    })

def login_user():
    return measure_request("Login", "POST", f"{BASE_URL}/users/login", {
        "email": email,
        "password": password
    })

def create_booking():
    response = measure_request("Booking", "POST", f"{BASE_URL}/bookings/create", {
        "user_id": 1,
        "event_id": 101,
        "event": "Music Concert",
        "date": "2025-06-01",
        "seats": 2
    })
    if response.status_code == 200:
        try:
            return response.json().get("id")
        except:
            return None
    return None

def create_payment(booking_id):
    return measure_request("Payment", "POST", f"{BASE_URL}/payments/create", {
        "booking_id": booking_id,
        "amount": 150.0,
        "payment_method": "credit_card",
        "user_id": 1,
        "method": "credit_card",
        "status": "paid"
    })

def print_summary(start_time, end_time, cpu_before, cpu_after, mem_before, mem_after):
    total_time = round(end_time - start_time, 3)
    total_sent = sum(r["sent"] for r in results)
    total_received = sum(r["received"] for r in results)
    total_requests = len(results)
    total_success = sum(1 for r in results if r["success"])
    total_failures = total_requests - total_success
    avg_response = round(sum(r["time"] for r in results) / total_requests, 3)
    max_response = max(r["time"] for r in results)
    min_response = min(r["time"] for r in results)
    rps = round(total_requests / total_time, 2) if total_time > 0 else "N/A"

    print("\n📊 Performance Summary:")
    print(f"Total Requests: {total_requests}")
    print(f"✔️ Success Rate: {round((total_success / total_requests) * 100, 1)}%")
    print(f"❌ Error Rate: {round((total_failures / total_requests) * 100, 1)}%")
    print(f"⏱️ Avg Response Time: {avg_response}s | Max: {max_response}s | Min: {min_response}s")
    print(f"📤 Total Payload Sent: {total_sent} B")
    print(f"📥 Total Payload Received: {total_received} B")
    print(f"🚀 Throughput (RPS): {rps} requests/sec")
    print(f"🧠 Memory Before: {mem_before / 1024 / 1024:.2f} MB | After: {mem_after / 1024 / 1024:.2f} MB")
    print(f"⚙️ CPU Usage Before: {cpu_before}% | After: {cpu_after}%")


def run_test():
    # Before metrics
    process = psutil.Process(os.getpid())
    cpu_before = psutil.cpu_percent(interval=1)
    mem_before = process.memory_info().rss
    start_time = time.time()

    # API calls
    register_user()
    login_user()
    booking_id = create_booking()
    if booking_id:
        create_payment(booking_id)
    else:
        print("❌ Booking creation failed.")

    # After metrics
    end_time = time.time()
    cpu_after = psutil.cpu_percent(interval=1)
    mem_after = process.memory_info().rss

    print_summary(start_time, end_time, cpu_before, cpu_after, mem_before, mem_after)

if __name__ == "__main__":
    run_test()
