import grpc
from app.grpc_services import user_pb2, user_pb2_grpc

def run():
    channel = grpc.insecure_channel("localhost:50051")
    stub = user_pb2_grpc.UserServiceStub(channel)

    print("\n📤 Trying to register...")
    register_response = stub.Register(user_pb2.RegisterRequest(
        email="osama@gmail.com",
        username="osama",
        password="123456"
    ))
    print("✅ Register Response:", register_response.message)

    print("\n📤 Trying to login...")
    login_response = stub.Login(user_pb2.LoginRequest(
        email="osama@gmail.com",
        password="123456"
    ))
    print("✅ Login Response:", login_response.message)

if __name__ == "__main__":
    run()
