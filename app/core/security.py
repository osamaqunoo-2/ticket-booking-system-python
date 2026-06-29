from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, stored_password: str) -> bool:
    if stored_password.startswith("$2"):
        return pwd_context.verify(plain_password, stored_password)

    return plain_password == stored_password
