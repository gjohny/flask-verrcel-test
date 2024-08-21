import os


class Config:
    SECRET_KEY = os.getenv('secret_user_key', os.urandom(24))
    SQLALCHEMY_DATABASE_URI = os.getenv('Database_URL', 'postgresql://default:jJx2GPQWH9Yg@ep-silent-butterfly-a4hqfavj-pooler.us-east-1.aws.neon.tech:5432/verceldb?sslmode=require')