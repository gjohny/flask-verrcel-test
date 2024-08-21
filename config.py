import os


class Config:
    SECRET_KEY = os.getenv('secret_user_key', os.urandom(24))
    SQLALCHEMY_DATABASE_URI = os.getenv('Database_URL', 'comig soon postfres_url_here')