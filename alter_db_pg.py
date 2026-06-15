from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

def alter():
    load_dotenv("d:/Screener/.env")
    engine = create_engine(os.getenv("DATABASE_URL"))
    with engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN phone_number VARCHAR(20)"))
        except Exception as e:
            print(f"Error 1: {e}")
        try:
            conn.execute(text("ALTER TABLE users ADD COLUMN sms_alerts_enabled BOOLEAN DEFAULT FALSE"))
        except Exception as e:
            print(f"Error 2: {e}")
        conn.commit()
    print("Database altered successfully")

if __name__ == "__main__":
    alter()
