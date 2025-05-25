import requests
import time

class GraphQLPerformanceTester:
    def __init__(self, base_url):
        self.base_url = base_url

    def send_graphql(self, query_body):
        start = time.time()
        response = requests.post(self.base_url, json={"query": query_body})
        end = time.time()
        print(f"⏱️ Took: {round((end - start)*1000, 2)} ms")
        print(response.status_code, response.text)
        return response

    def register_user(self):
        query = """
        mutation {
          registerUser(email: "test@example.com", username: "tester", password: "123456")
        }
        """
        print("\n🔹 Register User")
        return self.send_graphql(query)

    def login_user(self):
        query = """
        mutation {
          loginUser(email: "test@example.com", password: "123456")
        }
        """
        print("\n🔹 Login User")
        return self.send_graphql(query)

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
        print("\n🔹 Create Booking")
        return self.send_graphql(query)

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
        print("\n🔹 Create Payment")
        return self.send_graphql(query)

    def run_test(self):
        self.register_user()
        self.login_user()
        self.create_booking()
        self.create_payment()


if __name__ == "__main__":
    tester = GraphQLPerformanceTester("http://localhost:8000/graphql")
    tester.run_test()
