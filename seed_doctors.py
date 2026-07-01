from app import app
from extensions import db
from models.doctor import Doctor

doctors = [
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
    for doctor in doctors:
        exists = Doctor.query.filter_by(email=doctor["email"]).first()

        if not exists:
            new_doctor = Doctor(
                name=doctor["name"],
                specialization=doctor["specialization"],
                email=doctor["email"],
                password=doctor["password"]
            )
            db.session.add(new_doctor)

    db.session.commit()
    print("Doctors seeded successfully!")