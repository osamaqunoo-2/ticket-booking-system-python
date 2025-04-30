import grpc
from concurrent import futures
from app.grpc_services import user_pb2_grpc
from app.grpc_services.user_service import UserService

def serve():
    print("🔥 server script started")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port("[::]:50051")
    print("gRPC server is running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
