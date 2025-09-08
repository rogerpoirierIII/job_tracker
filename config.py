import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///jobs.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
