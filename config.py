import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "gm_hospital_secret_key_2026")

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:plsql@localhost:5432/gm_hospital"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024

    AWS_REGION = os.environ.get("AWS_REGION", "ap-south-1")
    S3_BUCKET = os.environ.get("S3_BUCKET")
