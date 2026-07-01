import os

class Config:
    SECRET_KEY = "gm_hospital_secret_key"

    SQLALCHEMY_DATABASE_URI = (
        "postgresql://postgres:plsql@localhost:5432/gm_hospital"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False