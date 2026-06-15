import sqlite3

def alter():
    conn = sqlite3.connect("d:/Screener/sqlite.db")
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN phone_number VARCHAR(20)")
    except Exception as e:
        print(f"Error adding phone_number: {e}")
        
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN sms_alerts_enabled BOOLEAN DEFAULT 0")
    except Exception as e:
        print(f"Error adding sms_alerts_enabled: {e}")
        
    conn.commit()
    conn.close()
    print("Database altered successfully")

if __name__ == "__main__":
    alter()
