from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


# رابط الاتصال بقاعدة البيانات
DATABASE_URL = "postgresql://admin:admin@db:5432/ticket_db"
#DATABASE_URL = "postgresql://admin:admin@localhost:5432/ticket_db"
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin@localhost:5432/ticket_db")


# إنشاء محرك الاتصال
engine = create_engine(DATABASE_URL)

# إعداد جلسات العمل مع القاعدة
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# القاعدة الأساسية لتعريف الجداول
Base = declarative_base()
