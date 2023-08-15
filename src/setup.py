from dotenv import load_dotenv
import os
load_dotenv()

user = os.getenv("DB_USER") or ""
password = os.getenv("DB_PASSWORD") or ""
host = os.getenv("DB_HOST") or ""
database = os.getenv("DB_NAME") or ""
token = os.getenv("TOKEN") or ""
owner = int(os.getenv("OWNER") or "0")