import grpc
from concurrent import futures
from app.grpc_services import user_pb2_grpc
from app.grpc_services.user_service import UserService
from app.grpc_services.booking_service import BookingService
from app.grpc_services import booking_pb2_grpc


def serve():
    print("🔥 server script started")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    booking_pb2_grpc.add_BookingServiceServicer_to_server(BookingService(), server)
    server.add_insecure_port("[::]:50051")
    print("gRPC server is running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
