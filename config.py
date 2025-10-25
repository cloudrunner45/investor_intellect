import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")
    STOCK_API_KEY = os.getenv("STOCK_API_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
