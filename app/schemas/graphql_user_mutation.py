import graphene
from graphene import String, Boolean
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from models.user_model import User as UserModel
from passlib.hash import bcrypt
from schemas.user_schema import UserCreate, UserLogin


class RegisterUser(graphene.Mutation):
    class Arguments:
        email = String(required=True)
        username = String(required=True)
        password = String(required=True)

    success = Boolean()
    message = String()

    def mutate(self, info, email, username, password):
        try:
            # التحقق من القيم باستخدام Pydantic
            validated = UserCreate(email=email, username=username, password=password)
        except Exception as e:
            return RegisterUser(success=False, message=str(e))

        db: Session = SessionLocal()
        if db.query(UserModel).filter(UserModel.email == validated.email).first():
            return RegisterUser(success=False, message="Email already exists")

        user = UserModel(
            email=validated.email,
            username=validated.username,
            password=bcrypt.hash(validated.password)
        )
        db.add(user)
        db.commit()
        return RegisterUser(success=True, message="User registered successfully")


class LoginUser(graphene.Mutation):
    class Arguments:
        email = String(required=True)
        password = String(required=True)

    success = Boolean()
    message = String()
    token = String()

    def mutate(self, info, email, password):
        try:
            validated = UserLogin(email=email, password=password)
        except Exception as e:
            return LoginUser(success=False, message=str(e), token="")

        db: Session = SessionLocal()
        user = db.query(UserModel).filter(UserModel.email == validated.email).first()
        if not user or not bcrypt.verify(validated.password, user.password):
            return LoginUser(success=False, message="Invalid credentials", token="")
        
        token = "dummy-token"
        return LoginUser(success=True, message="Login successful", token=token)


class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
    login_user = LoginUser.Field()
