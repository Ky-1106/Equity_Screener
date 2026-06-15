from backend.database import SessionLocal
from backend.main import schemas
from backend.main import register

db = SessionLocal()
try:
    user = schemas.UserCreate(email="test3@crash.com", password="password")
    register(user=user, db=db)
    print("Success")
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()
