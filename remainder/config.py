import os
from os.path import join, dirname
from dotenv import load_dotenv


class Config:
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or os.environ.get('LOCAL_POSTGRESQL_URI')
    if SQLALCHEMY_DATABASE_URI is not None:
        if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
            SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
