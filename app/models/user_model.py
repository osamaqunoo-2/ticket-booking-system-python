from sqlalchemy import Column, Integer, String
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)  # 👈 ضروري
    username = Column(String, nullable=False)                        # 👈 ضروري
    password = Column(String, nullable=False)