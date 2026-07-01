from flask_login import UserMixin
from extensions import db


class Doctor(UserMixin, db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    appointments = db.relationship("Appointment", back_populates="doctor", lazy=True)

    @property
    def role(self):
        return "doctor"

    def get_id(self):
        return f"doctor:{self.id}"

    def __repr__(self):
        return f"<Doctor {self.name}>"
