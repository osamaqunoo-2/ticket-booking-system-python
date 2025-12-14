▶️ Run the Full Project
🔹 Run the project with a clean database (remove all stored data)
docker-compose down --volumes
docker-compose up --build

🔹 Run the project without deleting data or database
docker-compose down
docker-compose up --build

🔌 gRPC Services
Activate the virtual environment (Windows)
.\venv\Scripts\Activate.ps1

Run the gRPC client
python -m app.grpc_services.client

Run the gRPC server
python -m app.grpc_services.server

Stop the gRPC server (Windows)
taskkill /PID 5768 /F

🟢 Check Which Process Is Using Port 50051
netstat -aon | findstr :50051

📄 View Docker Container Logs
docker-compose logs app

🌐 API Endpoints

GraphQL Playground:
http://localhost:8000/graphql

REST API (Swagger UI):
http://localhost:8000/docs

🧾 Git Workflow
git add .
git commit -m "create test script"
git push origin main
