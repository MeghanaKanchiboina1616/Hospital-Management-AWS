from werkzeug.security import generate_password_hash

from app import app
from extensions import db
from models.doctor import Doctor

DOCTORS = [
    {
        "name": "Dr. Ravi Kumar",
        "specialization": "General Physician",
        "email": "ravi@gmhospital.com",
        "password": "ravi123"
    },
    {
        "name": "Dr. Sneha Reddy",
        "specialization": "Orthopedic Surgeon",
        "email": "sneha@gmhospital.com",
        "password": "sneha123"
    },
    {
        "name": "Dr. Arjun Mehta",
        "specialization": "Oncologist",
        "email": "arjun@gmhospital.com",
        "password": "arjun123"
    }
]

with app.app_context():
    db.create_all()

    for doctor in DOCTORS:
        existing = Doctor.query.filter_by(email=doctor["email"]).first()
        password_hash = generate_password_hash(doctor["password"])

        if existing:
            existing.name = doctor["name"]
            existing.specialization = doctor["specialization"]
            existing.password = password_hash
        else:
            db.session.add(Doctor(
                name=doctor["name"],
                specialization=doctor["specialization"],
                email=doctor["email"],
                password=password_hash
            ))

    db.session.commit()
    print("Doctors seeded successfully.")
