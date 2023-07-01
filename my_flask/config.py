from datetime import timedelta


class Config:
    DEBUG = True
    SECRET_KEY = 'DianeDiana'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)