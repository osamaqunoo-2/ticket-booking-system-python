# استخدم صورة بايثون الرسمية
FROM python:3.11-slim

# إنشاء مجلد داخل الكونتينر
WORKDIR /app

# نسخ ملفات المشروع إلى الكونتينر
COPY . .

# تثبيت مكتبات المشروع
RUN pip install --no-cache-dir -r requirements.txt

# الأمر الافتراضي لتشغيل السيرفر (لاحقاً نعدل عليه حسب السيرفر)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]