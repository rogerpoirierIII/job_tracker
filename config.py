import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///jobs.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False