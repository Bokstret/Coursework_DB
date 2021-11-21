import os


class Config():
    SQLACHEMY_DATABASE_URI = os.environ['DB_LINK']
    SECRET_KEY = b'\xb2Ee\x0f\xdf5\xcf\x00\xc3\x81a\xd5'
