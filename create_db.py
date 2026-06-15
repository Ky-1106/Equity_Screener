import os
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load from .env
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
db_url = os.getenv("DATABASE_URL")

# Parse the URL
parsed_url = urlparse(db_url)
username = parsed_url.username
password = parsed_url.password
hostname = parsed_url.hostname
port = parsed_url.port
database_name = parsed_url.path.lstrip('/')

print(f"Connecting to default 'postgres' database to create new database: {database_name}...")

try:
    # Connect to the default 'postgres' database to issue the CREATE DATABASE command
    conn = psycopg2.connect(
        dbname="postgres",
        user=username,
        password=password,
        host=hostname,
        port=port
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Try creating the database
    cursor.execute(f"CREATE DATABASE {database_name};")
    print(f"Successfully created database: {database_name}")
    
except psycopg2.errors.DuplicateDatabase:
    print(f"Database {database_name} already exists.")
except Exception as e:
    print(f"Error creating database: {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
