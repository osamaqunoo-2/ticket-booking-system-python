#لتشغيل المشروع كلو 
docker-compose down --volumes
docker-compose up --build

لاعادة تشغيل المشروع بدون حذف كل البيانات والداتا بيز 
docker-compose down
docker-compose up --build

#لتشغيل gRPC
#.\venv\Scripts\Activate.ps1 
##python -m app.grpc_services.client



لفتح اللوج الحاوية 
docker-compose logs app


http://localhost:8000/graphql
http://localhost:8000/docs