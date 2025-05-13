FROM python:3.11

# إعداد مجلد العمل
WORKDIR /app

# تثبيت أدوات البناء اللازمة (هامة لـ grpcio/bcrypt)
RUN apt-get update && apt-get install -y build-essential gcc

# تثبيت المتطلبات
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# نسخ ملفات المشروع
COPY . .

# أمر التشغيل
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
