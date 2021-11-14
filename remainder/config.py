import os
from os.path import join, dirname
from dotenv import load_dotenv


class Config:
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or "postgresql://localhost/remainder"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
