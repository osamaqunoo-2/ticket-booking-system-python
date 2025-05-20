echo "🔍 Collecting Environment Info..."

# نستخدم python بدل python3 لأنك على Windows
winpty python env_info.py

echo "✅ Environment Info collected."
#echo "🏁 Starting REST Load Test..."
#locust -f rest_test.py --headless -u 100 -r 10 -t30s --host=http://localhost:8000

#echo "🏁 Starting gRPC Load Test..."
#locust -f grpc_test.py --headless -u 100 -r 10 -t30s

#echo "🏁 Starting GraphQL Load Test..."
#locust -f graphql_test.py --headless -u 100 -r 10 -t30s --host=http://localhost:4000/graphql