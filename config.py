import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://jobtracker_db_guzr_user:LXFT8RVF7ygeV5MMW3Odw4bhKD41ZuGW@dpg-d2v4fa3uibrs7387dsa0-a/jobtracker_db_guzr")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
