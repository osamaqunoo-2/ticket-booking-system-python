import grpc
from concurrent import futures
from app.grpc_services import user_pb2_grpc
from app.grpc_services.user_service import UserService

from app.grpc_services import booking_pb2_grpc
from app.grpc_services.booking_service import BookingService

from app.grpc_services import payment_pb2_grpc             # ✅ 1. استيراد ملفات الدفع
from app.grpc_services.payment_service import PaymentService  # ✅ 2. استيراد كلاس الخدمة

def serve():
    print("🔥 server script started")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    booking_pb2_grpc.add_BookingServiceServicer_to_server(BookingService(), server)
    payment_pb2_grpc.add_PaymentServiceServicer_to_server(PaymentService(), server)  # ✅ 3. تسجيل خدمة الدفع

    server.add_insecure_port("[::]:50051")
    print("gRPC server is running on port 50051...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
