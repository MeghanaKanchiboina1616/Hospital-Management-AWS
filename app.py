from flask import Flask, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user

from config import Config
from extensions import db, migrate, login_manager
from forms import RegistrationForm, LoginForm
from models.patient import Patient
import models

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return Patient.query.get(int(user_id))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        patient = Patient(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            password=generate_password_hash(form.password.data)
        )

        db.session.add(patient)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        patient = Patient.query.filter_by(email=form.email.data).first()

        if patient and check_password_hash(patient.password, form.password.data):
            login_user(patient)
            return redirect(url_for("patient_dashboard"))

    return render_template("login.html", form=form)


@app.route("/patient-dashboard")
@login_required
def patient_dashboard():
    return f"Welcome, {current_user.name}!"


if __name__ == "__main__":
    app.run(debug=True)