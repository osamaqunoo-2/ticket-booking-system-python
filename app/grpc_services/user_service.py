from app.grpc_services import user_pb2, user_pb2_grpc
from app.models.user_model import User
from app.core.database import SessionLocal
from sqlalchemy.orm import Session

class UserService(user_pb2_grpc.UserServiceServicer):
    def Register(self, request, context):
        db: Session = SessionLocal()
        existing_user = db.query(User).filter(User.email == request.email).first()

        if existing_user:
            return user_pb2.UserResponse(message="Email already registered")

        new_user = User(email=request.email, username=request.username, password=request.password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return user_pb2.UserResponse(message="User registered successfully")

    def Login(self, request, context):
        db: Session = SessionLocal()
        user = db.query(User).filter(User.email == request.email).first()

        if user and user.password == request.password:
            return user_pb2.LoginResponse(message="Login successful")
        return user_pb2.LoginResponse(message="Invalid credentials")
