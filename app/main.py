from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import user
from app.core.database import Base, engine
from app.models import user_model
import threading
from app.grpc_services.server import serve

# Strawberry
from app.schemas.graphql_schema import schema
from strawberry.fastapi import GraphQLRouter

# إضافات التحقق من قاعدة البيانات
import psycopg2
import time

# التحقق من جاهزية قاعدة البيانات (Retry)
print("⏳ Checking if database is ready...")
for attempt in range(10):
    try:
        conn = psycopg2.connect(
            host="db",
            port=5432,
            user="admin",
            password="admin",
            dbname="ticket_db"
        )
        print("✅ Database is ready.")
        conn.close()
        break
    except psycopg2.OperationalError:
        print(f"❌ DB not ready (attempt {attempt + 1}/10) - retrying...")
        time.sleep(2)
else:
    print("❌ Could not connect to the database after multiple attempts.")
    exit(1)

# إنشاء الجداول
Base.metadata.create_all(bind=engine)

# إنشاء التطبيق
app = FastAPI()

# REST routes
app.include_router(user.router, prefix="/users", tags=["Users"])

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REST root
@app.get("/")
def root():
    return {"message": "Welcome to Ticket Booking System API! 🎟️"}

# GraphQL route
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# gRPC server في خيط منفصل
threading.Thread(target=serve, daemon=True).start()
