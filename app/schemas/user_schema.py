from pydantic import BaseModel, EmailStr



class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserOut(BaseModel):
    username: str
    email: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str