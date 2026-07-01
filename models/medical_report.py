from datetime import datetime

from extensions import db


class MedicalReport(db.Model):
    __tablename__ = "medical_reports"

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey("appointments.id"), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    s3_key = db.Column(db.String(500), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)

    patient = db.relationship("Patient", back_populates="reports")
    appointment = db.relationship("Appointment", back_populates="reports")
