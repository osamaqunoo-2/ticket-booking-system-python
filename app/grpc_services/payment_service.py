import grpc
from app.grpc_services import payment_pb2, payment_pb2_grpc
from app.models.payment_model import Payment
from app.core.database import SessionLocal

from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime

class PaymentService(payment_pb2_grpc.PaymentServiceServicer):

    def CreatePayment(self, request, context):
        db = SessionLocal()
        try:
            new_payment = Payment(
                user_id=request.user_id,
                booking_id=request.booking_id,
                amount=request.amount,
                method=request.method,
                status=request.status
            )
            db.add(new_payment)
            db.commit()
            db.refresh(new_payment)

            return payment_pb2.PaymentResponse(
                message="Payment created successfully!",
                success=True
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return payment_pb2.PaymentResponse(
                message="Failed to create payment",
                success=False
            )
        finally:
            db.close()

    def DeletePayment(self, request, context):
        db = SessionLocal()
        try:
            payment = db.query(Payment).filter(Payment.id == request.payment_id).first()
            if not payment:
                return payment_pb2.PaymentResponse(
                    message="Payment not found.",
                    success=False
                )
            db.delete(payment)
            db.commit()
            return payment_pb2.PaymentResponse(
                message="Payment deleted.",
                success=True
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return payment_pb2.PaymentResponse(
                message="Failed to delete payment",
                success=False
            )
        finally:
            db.close()

    def GetAllPayments(self, request, context):
        db = SessionLocal()
        try:
            payments = db.query(Payment).all()
            for p in payments:
                grpc_payment = payment_pb2.Payment(
                    id=p.id,
                    user_id=p.user_id,
                    booking_id=p.booking_id,
                    amount=p.amount,
                    method=p.method,
                    status=p.status,
                    timestamp=p.timestamp if hasattr(p, "timestamp") else ""
                )
                yield grpc_payment
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
        finally:
            db.close()
