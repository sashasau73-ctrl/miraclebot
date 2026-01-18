import os
from dotenv import load_dotenv

DB_PATH = "miracle_db.db"
load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")
TAGS = os.getenv("TAGS").strip().split(", ")
