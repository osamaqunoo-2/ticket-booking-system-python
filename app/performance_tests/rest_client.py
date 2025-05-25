import requests

BASE_URL = "http://localhost:8000"
email = "testuser@example.com"
password = "test123"
username = "testuser"

def register_user():
    response = requests.post(f"{BASE_URL}/users/register", json={
        "email": email,
        "password": password,
        "username": username
    })
    print("🔹 Register:", response.status_code, response.text)

def login_user():
    response = requests.post(f"{BASE_URL}/users/login", json={
        "email": email,
        "password": password
    })
    print("🔹 Login:", response.status_code, response.text)

def create_booking():
    response = requests.post(f"{BASE_URL}/bookings/create", json={
        "user_id": 1,
        "event_id": 101,
         "event": "Music Concert",    
        "date": "2025-06-01",          
        "seats": 2
    })
    print("🔹 Booking:", response.status_code, response.text)
    if response.status_code == 200:
        return response.json().get("id")  # assuming it returns the booking ID
    return None

def create_payment(booking_id):
    response = requests.post(f"{BASE_URL}/payments/create", json={
         "booking_id": booking_id,
        "amount": 150.0,
        "payment_method": "credit_card",
        "user_id": 1,
        "method": "credit_card",     
        "status": "paid"            
    })
    print("🔹 Payment:", response.status_code, response.text)

def run_test():
    register_user()
    login_user()

    booking_id = create_booking()
    if not booking_id:
        print("❌ Booking creation failed.")
        return

    create_payment(booking_id)

if __name__ == "__main__":
    run_test()
