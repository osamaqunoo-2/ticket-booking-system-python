from sqlalchemy import inspect
from database import engine  # تأكد من المسار الصحيح حسب مشروعك

inspector = inspect(engine)
tables = inspector.get_table_names()

print("📦 الجداول الموجودة في قاعدة البيانات:")
for table in tables:
    print(f" - {table}")