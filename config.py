import os
from dotenv import load_dotenv

load_dotenv()  # reads .env from the working directory

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-key")
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
        f"@{os.environ.get('DB_HOST', '127.0.0.1')}:{os.environ.get('DB_PORT', '3306')}"
        f"/{os.environ['DB_NAME']}"
    )