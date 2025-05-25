#لتشغيل المشروع كلو 
docker-compose down --volumes
docker-compose up --build

لاعادة تشغيل المشروع بدون حذف كل البيانات والداتا بيز 
docker-compose down
docker-compose up --build

#لتشغيل gRPC
.\venv\Scripts\Activate.ps1 
python -m app.grpc_services.client

تشغيل السيرفر
python -m app.grpc_services.server
اغلاق السيرفر
taskkill /PID 5768 /F

🟢 1. شغّل هذا الأمر لمعرفة العملية التي تحتل المنفذ:

netstat -aon | findstr :50051



لفتح اللوج الحاوية 
docker-compose logs app


http://localhost:8000/graphql
http://localhost:8000/docs






git add .
git commit -m "create test script"
git push origin main
