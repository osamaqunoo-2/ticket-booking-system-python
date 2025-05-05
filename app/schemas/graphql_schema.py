import strawberry
from app.core.database import SessionLocal
from app.models.user_model import User as UserModel
from app.schemas.user_schema import UserCreate, UserLogin
from passlib.hash import bcrypt


@strawberry.type
class Mutation:
    @strawberry.mutation
    def register_user(self, email: str, username: str, password: str) -> str:
        try:
            user_data = UserCreate(email=email, username=username, password=password)
        except Exception as e:
            return f"❌ Invalid data: {str(e)}"

        db = SessionLocal()
        try:
            if db.query(UserModel).filter(UserModel.email == user_data.email).first():
                return "❌ Email already registered"

            new_user = UserModel(
                email=user_data.email,
                username=user_data.username,
                password=user_data.password  # استخدم bcrypt.hash(user_data.password) لو بدك تشفير
            )
            db.add(new_user)
            db.commit()
            return "✅ User registered successfully"
        finally:
            db.close()

    @strawberry.mutation
    def login_user(self, email: str, password: str) -> str:
        try:
            login_data = UserLogin(email=email, password=password)
        except Exception as e:
            return f"❌ Invalid input: {str(e)}"

        db = SessionLocal()
        try:
            db_user = db.query(UserModel).filter(UserModel.email == login_data.email).first()
            if not db_user:
                return "❌ Invalid email"

            if db_user.password != login_data.password:
                return "❌ Incorrect password"

            return "✅ Login successful"
        finally:
            db.close()


@strawberry.type
class Query:
    hello: str = "GraphQL is connected to database!"

schema = strawberry.Schema(query=Query, mutation=Mutation)
