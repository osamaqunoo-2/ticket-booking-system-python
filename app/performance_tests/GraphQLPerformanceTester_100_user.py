import requests
import time
import json
import psutil
import os
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "http://localhost:8000/graphql"
results = []

def generate_email(i):
    return f"gql_user{i}@example.com"

def send_graphql(label, query_body):
    start = time.time()
    try:
        response = requests.post(BASE_URL, json={"query": query_body}, timeout=10)
    except Exception as e:
        return {
            "label": label,
            "status": 0,
            "time": 0,
            "sent": 0,
            "received": 0,
            "success": False
        }

    end = time.time()
    time_taken = round(end - start, 3)
    payload_sent = len(json.dumps({"query": query_body}).encode('utf-8'))
    payload_received = len(response.content)
    success = 200 <= response.status_code < 300

    return {
        "label": label,
        "status": response.status_code,
        "time": time_taken,
        "sent": payload_sent,
        "received": payload_received,
        "success": success
    }

def perform_session(i):
    session_result = []

    email = generate_email(i)
    password = "test123"
    username = f"graphqlUser{i}"

    register_query = f"""
    mutation {{
      registerUser(email: "{email}", username: "{username}", password: "{password}")
    }}
    """
    session_result.append(send_graphql("Register", register_query))

    login_query = f"""
    mutation {{
      loginUser(email: "{email}", password: "{password}")
    }}
    """
    session_result.append(send_graphql("Login", login_query))

    booking_query = f"""
    mutation {{
      createBooking(booking: {{
        userId: 1,
        event: "GraphQL Load Test Event",
        date: "2025-06-01"
      }})
    }}
    """
    session_result.append(send_graphql("Booking", booking_query))

    payment_query = f"""
    mutation {{
      createPayment(payment: {{
        userId: 1,
        bookingId: 1,
        amount: 150.0,
        method: "credit_card",
        status: "paid"
      }})
    }}
    """
    session_result.append(send_graphql("Payment", payment_query))

    return session_result

def run_graphql_load_test(user_count=100):
    global results

    process = psutil.Process(os.getpid())
    cpu_before = psutil.cpu_percent(interval=1)
    mem_before = process.memory_info().rss
    start = time.time()

    all_results = []

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(perform_session, i) for i in range(user_count)]
        for future in as_completed(futures):
            all_results.extend(future.result())

    end = time.time()
    cpu_after = psutil.cpu_percent(interval=1)
    mem_after = process.memory_info().rss

    results = all_results
    print_graphql_summary(start, end, cpu_before, cpu_after, mem_before, mem_after)

def print_graphql_summary(start_time, end_time, cpu_before, cpu_after, mem_before, mem_after):
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

    print("\n📊 GraphQL Load Test Summary (100 Users):")
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
    run_graphql_load_test(user_count=100)
