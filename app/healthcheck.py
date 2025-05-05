import requests
import psycopg2
import docker
import grpc
from app.grpc_services import user_pb2, user_pb2_grpc

# إعدادات الاتصال
DB_HOST = "localhost"
DB_PORT = 5432
DB_USER = "admin"
DB_PASSWORD = "admin"
DB_NAME = "ticket_db"

API_URL = "http://localhost:8000/"
GRPC_HOST = "localhost:50051"

# 1. فحص حاويات Docker
def check_docker_containers():
    try:
        client = docker.from_env()
        containers = client.containers.list()
        container_names = [c.name for c in containers]
        print("✅ Docker is running. Active containers:")
        for name in container_names:
            print(f"  - {name}")
        return True
    except Exception as e:
        print("❌ Docker error:", e)
        return False

# 2. فحص API FastAPI
def check_api():
    try:
        r = requests.get(API_URL)
        if r.status_code == 200:
            print("✅ FastAPI is running. Root response:", r.json())
            return True
        else:
            print("❌ FastAPI returned status code:", r.status_code)
            return False
    except Exception as e:
        print("❌ API connection error:", e)
        return False

# 3. فحص قاعدة البيانات
def check_database():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME
        )
        print("✅ Database connection established.")
        conn.close()
        return True
    except Exception as e:
        print("❌ Database connection error:", e)
        return False

# 4. فحص gRPC
def check_grpc():
    try:
        channel = grpc.insecure_channel(GRPC_HOST)
        stub = user_pb2_grpc.UserServiceStub(channel)
        response = stub.Login(user_pb2.LoginRequest(email="test@test.com", password="123456"))
        print("✅ gRPC is running. Test Login response:", response.message)
        return True
    except grpc.RpcError as e:
        print("❌ gRPC Error:", e.details())
        return False
    except Exception as e:
        print("❌ gRPC connection error:", e)
        return False

# ========== تنفيذ الفحص ==========
print("\n🔍 Running health check for your Ticket Booking System...\n")

docker_ok = check_docker_containers()
api_ok = check_api()
db_ok = check_database()
grpc_ok = check_grpc()

if docker_ok and api_ok and db_ok and grpc_ok:
    print("\n🎉 All systems are up and running! ✅")
else:
    print("\n⚠️ One or more components failed. Check above logs. ❌")
