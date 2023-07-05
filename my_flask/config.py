from datetime import timedelta


class Config:
    DEBUG = True
    JWT_TOKEN_LOCATION = 'headers'
    JWT_SECRET_KEY = 'DianeDianahhhhhhhhhhhhhhhhhhhhhhhhhhhhhkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkhvffffffffffffffffffffffffffffffgcddddddddddfffffffffffffffffffffffffffxxxxxxxretyyyyyyyiiiiiiiiiiiiigfyuiiiiiiiiiiiiiiuifuu'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)