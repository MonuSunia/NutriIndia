from database.database import engine

try:
    with engine.connect() as conn:
        print("✅ Connected to MySQL successfully!")
except Exception as e:
    print("❌ Connection failed:")
    print(e)