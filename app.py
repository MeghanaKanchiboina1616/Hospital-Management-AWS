from datetime import date, datetime
import os

import boto3
from flask import Flask, flash, redirect, render_template, request, send_from_directory
from flask import url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from config import Config
from extensions import db, login_manager, migrate
from forms import AppointmentForm, LoginForm, RegistrationForm, StatusForm
from models.appointment import Appointment
from models.doctor import Doctor
from models.medical_report import MedicalReport
from models.patient import Patient
import models

app = Flask(__name__)
app.config.from_object(Config)

DEFAULT_DOCTORS = [
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

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    if not user_id:
        return None

    if ":" in user_id:
        role, record_id = user_id.split(":", 1)
        if role == "patient":
            return Patient.query.get(int(record_id))
        if role == "doctor":
            return Doctor.query.get(int(record_id))
        return None

    return Patient.query.get(int(user_id))


def patient_required():
    return current_user.is_authenticated and current_user.role == "patient"


def doctor_required():
    return current_user.is_authenticated and current_user.role == "doctor"


def initialize_database():
    db.create_all()

    for doctor_data in DEFAULT_DOCTORS:
        doctor = Doctor.query.filter_by(email=doctor_data["email"]).first()

        if doctor:
            doctor.name = doctor_data["name"]
            doctor.specialization = doctor_data["specialization"]
            if "$" not in doctor.password:
                doctor.password = generate_password_hash(doctor_data["password"])
        else:
            db.session.add(Doctor(
                name=doctor_data["name"],
                specialization=doctor_data["specialization"],
                email=doctor_data["email"],
                password=generate_password_hash(doctor_data["password"])
            ))

    db.session.commit()


def save_report(file_storage, patient_id, appointment_id):
    original_name = secure_filename(file_storage.filename)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    key = f"reports/patient-{patient_id}/appointment-{appointment_id}/{timestamp}-{original_name}"

    if app.config["S3_BUCKET"]:
        file_storage.stream.seek(0)
        boto3.client("s3", region_name=app.config["AWS_REGION"]).upload_fileobj(
            file_storage,
            app.config["S3_BUCKET"],
            key
        )
    else:
        local_path = os.path.join(app.config["UPLOAD_FOLDER"], key.replace("/", os.sep))
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        file_storage.save(local_path)

    return original_name, key


@app.route("/")
def home():
    doctors = Doctor.query.order_by(Doctor.name).all()
    return render_template("index.html", doctors=doctors)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        existing = Patient.query.filter_by(email=form.email.data.lower()).first()
        if existing:
            flash("An account already exists with that email.", "warning")
            return render_template("register.html", form=form)

        patient = Patient(
            name=form.name.data,
            email=form.email.data.lower(),
            phone=form.phone.data,
            password=generate_password_hash(form.password.data)
        )
        db.session.add(patient)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        patient = Patient.query.filter_by(email=form.email.data.lower()).first()
        if patient and check_password_hash(patient.password, form.password.data):
            login_user(patient)
            return redirect(url_for("patient_dashboard"))
        flash("Invalid patient email or password.", "danger")

    return render_template("login.html", form=form, title="Patient Login")


@app.route("/doctor-login", methods=["GET", "POST"])
def doctor_login():
    form = LoginForm()

    if form.validate_on_submit():
        doctor = Doctor.query.filter_by(email=form.email.data.lower()).first()
        if doctor and check_password_hash(doctor.password, form.password.data):
            login_user(doctor)
            return redirect(url_for("doctor_dashboard"))
        flash("Invalid doctor email or password.", "danger")

    return render_template("login.html", form=form, title="Doctor Login", doctor_login=True)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))


@app.route("/patient-dashboard")
@login_required
def patient_dashboard():
    if not patient_required():
        return redirect(url_for("doctor_dashboard"))

    appointments = Appointment.query.filter_by(patient_id=current_user.id).order_by(
        Appointment.appointment_date.desc(),
        Appointment.appointment_time.desc()
    ).all()
    upcoming = [item for item in appointments if item.appointment_date >= date.today()]
    history = [item for item in appointments if item.appointment_date < date.today()]

    return render_template(
        "patient_dashboard.html",
        patient=current_user,
        upcoming=upcoming,
        history=history
    )


@app.route("/book-appointment", methods=["GET", "POST"])
@login_required
def book_appointment():
    if not patient_required():
        return redirect(url_for("doctor_dashboard"))

    form = AppointmentForm()
    doctors = Doctor.query.order_by(Doctor.name).all()
    form.doctor.choices = [(doctor.id, f"{doctor.name} - {doctor.specialization}") for doctor in doctors]

    if not doctors:
        flash("No doctors are available yet. Run the doctor seed script first.", "warning")

    if form.validate_on_submit():
        appointment = Appointment(
            patient_id=current_user.id,
            doctor_id=form.doctor.data,
            appointment_date=form.appointment_date.data,
            appointment_time=form.appointment_time.data,
            status="Pending"
        )
        db.session.add(appointment)
        db.session.flush()

        if form.report.data and form.report.data.filename:
            file_name, key = save_report(form.report.data, current_user.id, appointment.id)
            appointment.report_filename = file_name
            db.session.add(MedicalReport(
                patient_id=current_user.id,
                appointment_id=appointment.id,
                file_name=file_name,
                s3_key=key
            ))

        db.session.commit()
        flash("Appointment booked successfully.", "success")
        return redirect(url_for("my_appointments"))

    return render_template("book_appointment.html", form=form)


@app.route("/my-appointments")
@login_required
def my_appointments():
    if not patient_required():
        return redirect(url_for("doctor_dashboard"))

    appointments = Appointment.query.filter_by(patient_id=current_user.id).order_by(
        Appointment.appointment_date.desc(),
        Appointment.appointment_time.desc()
    ).all()
    return render_template("my_appointments.html", appointments=appointments)


@app.route("/doctor-dashboard")
@login_required
def doctor_dashboard():
    if not doctor_required():
        return redirect(url_for("patient_dashboard"))

    todays_appointments = Appointment.query.filter_by(
        doctor_id=current_user.id,
        appointment_date=date.today()
    ).order_by(Appointment.appointment_time).all()
    appointments = Appointment.query.filter_by(doctor_id=current_user.id).order_by(
        Appointment.appointment_date.desc(),
        Appointment.appointment_time.desc()
    ).all()

    return render_template(
        "doctor_dashboard.html",
        appointments=appointments,
        todays_appointments=todays_appointments
    )


@app.route("/doctor/appointments/<int:appointment_id>", methods=["GET", "POST"])
@login_required
def appointment_detail(appointment_id):
    if not doctor_required():
        return redirect(url_for("patient_dashboard"))

    appointment = Appointment.query.filter_by(
        id=appointment_id,
        doctor_id=current_user.id
    ).first_or_404()
    form = StatusForm()
    if request.method == "GET":
        form.status.data = appointment.status

    if form.validate_on_submit():
        appointment.status = form.status.data
        db.session.commit()
        flash("Appointment status updated.", "success")
        return redirect(url_for("appointment_detail", appointment_id=appointment.id))

    return render_template("appointment_detail.html", appointment=appointment, form=form)


@app.route("/reports/<int:report_id>/download")
@login_required
def download_report(report_id):
    report = MedicalReport.query.get_or_404(report_id)
    allowed_patient = current_user.role == "patient" and report.patient_id == current_user.id
    allowed_doctor = current_user.role == "doctor" and report.appointment.doctor_id == current_user.id

    if not (allowed_patient or allowed_doctor):
        flash("You do not have access to that report.", "danger")
        return redirect(url_for("home"))

    if app.config["S3_BUCKET"]:
        url = boto3.client("s3", region_name=app.config["AWS_REGION"]).generate_presigned_url(
            "get_object",
            Params={"Bucket": app.config["S3_BUCKET"], "Key": report.s3_key},
            ExpiresIn=300
        )
        return redirect(url)

    local_dir = os.path.join(app.config["UPLOAD_FOLDER"], os.path.dirname(report.s3_key))
    return send_from_directory(local_dir, os.path.basename(report.s3_key), as_attachment=True)


with app.app_context():
    initialize_database()


if __name__ == "__main__":
    app.run(debug=True)
