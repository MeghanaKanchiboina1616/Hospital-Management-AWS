from flask_login import UserMixin
from extensions import db


class Patient(UserMixin, db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    appointments = db.relationship("Appointment", back_populates="patient", lazy=True)
    reports = db.relationship("MedicalReport", back_populates="patient", lazy=True)

    @property
    def role(self):
        return "patient"

    def get_id(self):
        return f"patient:{self.id}"
