from fastapi import APIRouter
from app.schemas.user_schema import UserCreate, UserOut,UserLogin

router = APIRouter()

users = []

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate):
    users.append(user)
    return user

@router.get("/users", response_model=list[UserOut])
def get_users():
    return users

@router.post("/login")
def login_user(login_data: UserLogin):
    for user in users:
        if user.username == login_data.username and user.password == login_data.password:
            return {"message": "Login successful", "user": user}
    raise HTTPException(status_code=401, detail="Invalid username or password")