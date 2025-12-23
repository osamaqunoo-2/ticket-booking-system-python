import requests
import time
import json
import psutil
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import random

BASE_URL = "http://localhost:8000"
results = []

def generate_email(i):
    return f"testuser{i}@example.com"

def measure_session(i):
    session_result = []
    email = generate_email(i)
    password = "test123"
    username = f"user{i}"

    def measure_request(label, method, url, json_data=None):
        start = time.time()
        try:
            response = requests.request(method, url, json=json_data, timeout=10)
        except Exception as e:
            session_result.append({
                "label": label,
                "status": 0,
                "time": 0,
                "sent": 0,
                "received": 0,
                "success": False
            })
            return
        end = time.time()
        time_taken = round(end - start, 3)
        payload_sent = len(json.dumps(json_data or {}).encode('utf-8'))
        payload_received = len(response.content)
        success = 200 <= response.status_code < 300

        session_result.append({
            "label": label,
            "status": response.status_code,
            "time": time_taken,
            "sent": payload_sent,
            "received": payload_received,
            "success": success
        })

    try:
        measure_request("Register", "POST", f"{BASE_URL}/users/register", {
            "email": email,
            "password": password,
            "username": username
        })
        measure_request("Login", "POST", f"{BASE_URL}/users/login", {
            "email": email,
            "password": password
        })
        response = requests.post(f"{BASE_URL}/bookings/create", json={
            "user_id": 1,
            "event_id": random.randint(100, 999),
            "event": "Concert",
            "date": "2025-06-01",
            "seats": 2
        })
        booking_id = None
        if response.status_code == 200:
            try:
                booking_id = response.json().get("id")
            except:
                pass
        session_result.append({
            "label": "Booking",
            "status": response.status_code,
            "time": round(response.elapsed.total_seconds(), 3),
            "sent": len(json.dumps(response.request.body or '').encode('utf-8')),
            "received": len(response.content),
            "success": response.status_code == 200
        })

        if booking_id:
            response = requests.post(f"{BASE_URL}/payments/create", json={
                "booking_id": booking_id,
                "amount": 150.0,
                "payment_method": "credit_card",
                "user_id": 1,
                "method": "credit_card",
                "status": "paid"
            })
            session_result.append({
                "label": "Payment",
                "status": response.status_code,
                "time": round(response.elapsed.total_seconds(), 3),
                "sent": len(json.dumps(response.request.body or '').encode('utf-8')),
                "received": len(response.content),
                "success": response.status_code == 200
            })
    except Exception as e:
        pass

    return session_result

def run_load_test(user_count):
    global results
    process = psutil.Process(os.getpid())
    cpu_before = psutil.cpu_percent(interval=1)
    mem_before = process.memory_info().rss
    start = time.time()

    all_results = []

    with ThreadPoolExecutor(max_workers=200) as executor:
        futures = [executor.submit(measure_session, i) for i in range(user_count)]
        for future in as_completed(futures):
            all_results.extend(future.result())

    end = time.time()
    cpu_after = psutil.cpu_percent(interval=1)
    mem_after = process.memory_info().rss

    results = all_results
    print_summary(start, end, cpu_before, cpu_after, mem_before, mem_after)

def print_summary(start_time, end_time, cpu_before, cpu_after, mem_before, mem_after):
    total_time = round(end_time - start_time, 3)
    total_sent = sum(r["sent"] for r in results)
    total_received = sum(r["received"] for r in results)
    total_requests = len(results)
    total_success = sum(1 for r in results if r["success"])
    total_failures = total_requests - total_success
    avg_response = round(sum(r["time"] for r in results) / total_requests, 3) if total_requests else 0
    max_response = max((r["time"] for r in results), default=0)
    min_response = min((r["time"] for r in results), default=0)
    rps = round(total_requests / total_time, 2) if total_time > 0 else "N/A"

    estimated_users = int(total_requests / 4)
    print(f"\n📊 Load Test Summary (~{estimated_users} Users):")
    print(f"Total Requests: {total_requests}")
    print(f"✔️ Success Rate: {round((total_success / total_requests) * 100, 1)}%")
    print(f"❌ Error Rate: {round((total_failures / total_requests) * 100, 1)}%")
    print(f"⏱️ Avg Response Time: {avg_response}s | Max: {max_response}s | Min: {min_response}s")
    print(f"📤 Total Payload Sent: {total_sent / 1024:.2f} KB")
    print(f"📥 Total Payload Received: {total_received / 1024:.2f} KB")
    print(f"🚀 Throughput (RPS): {rps} requests/sec")
    print(f"🧠 Memory Before: {mem_before / 1024 / 1024:.2f} MB | After: {mem_after / 1024 / 1024:.2f} MB")
    print(f"⚙️ CPU Usage Before: {cpu_before}% | After: {cpu_after}%")

if __name__ == "__main__":
    run_load_test(500)
