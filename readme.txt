# Microservices API Performance Comparison (REST vs GraphQL vs gRPC)

This project evaluates and compares the performance of three common API technologies used for microservice communication:
- REST
- GraphQL
- gRPC

The system implements a transactional microservice workflow using functionally identical service variants. Performance is measured using response time, throughput, CPU/memory utilization, payload size, and success rate under different user-load levels.

---

## ▶️ Run the Full Project

### 🔹 Run the project with a clean database (remove all stored data)
```bash
docker-compose down --volumes
docker-compose up --build
🔹 Run the project without deleting data or database
bash
Copy code
docker-compose down
docker-compose up --build
📄 View Docker Container Logs
bash
Copy code
docker-compose logs app
🌐 API Endpoints
GraphQL Playground
bash
Copy code
http://localhost:8000/graphql
REST API (Swagger UI)
bash
Copy code
http://localhost:8000/docs
🔌 gRPC Services
✅ Activate the virtual environment (Windows)
powershell
Copy code
.\venv\Scripts\Activate.ps1
✅ Run the gRPC server
bash
Copy code
python -m app.grpc_services.server
✅ Run the gRPC client
bash
Copy code
python -m app.grpc_services.client
🛑 Stop the gRPC server (Windows)
Replace <PID> with the actual process ID.

bash
Copy code
taskkill /PID <PID> /F
🟢 Check which process is using port 50051 (Windows)
bash
Copy code
netstat -aon | findstr :50051
🧪 Performance Test Scripts
Performance experiments are located under:

Copy code
performance_tests/
✅ Variable-load testing approach (Important Note)
Intermediate user-load levels (e.g., 200–900 concurrent users) were executed by modifying the user count parameter internally within the same test script, rather than creating a separate script file for each load level.
This approach was used to maintain a consistent test harness and avoid duplicated scripts while still executing all required load scenarios.

Adopted test script names
REST:
rest_client_variable_load.py

GraphQL:
GraphQLPerformanceTester_variable_load.py

gRPC:
grpc_performance_tester_variable_load.py

These scripts were used to run multiple load scenarios by updating the configured concurrent user value inside the script when needed.

🧾 Git Workflow
bash
Copy code
git add .
git commit -m "Finalize performance evaluation and results"
git push origin main
