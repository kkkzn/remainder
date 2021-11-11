import os
from os.path import join, dirname
from dotenv import load_dotenv


class Config:
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI_REMAINDER')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
