import os


class Config():
    SQLACHEMY_DATABASE_URI = os.environ['DB_LINK']
    SECRET_KEY = os.environ['SECRET_KEY']
