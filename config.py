import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DB_HOST = os.environ.get('DB_HOST') or 'localhost'
    DB_USER = os.environ.get('DB_USER') or 'your_username'
    DB_PASSWORD = os.environ.get('DB_PASSWORD') or 'your_password'
    DB_NAME = os.environ.get('DB_NAME') or 'your_database'