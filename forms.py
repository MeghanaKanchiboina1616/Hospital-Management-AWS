from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileSize
from wtforms import DateField, FileField, PasswordField, SelectField, StringField
from wtforms import SubmitField, TimeField
from wtforms.validators import DataRequired, Email, Length


class RegistrationForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(max=100)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone Number", validators=[DataRequired(), Length(max=15)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class AppointmentForm(FlaskForm):
    doctor = SelectField("Select Doctor", coerce=int, validators=[DataRequired()])
    appointment_date = DateField("Appointment Date", validators=[DataRequired()])
    appointment_time = TimeField("Appointment Time", validators=[DataRequired()])
    report = FileField(
        "Previous Medical Report",
        validators=[
            FileAllowed(["pdf", "png", "jpg", "jpeg"], "PDF or image only."),
            FileSize(max_size=10 * 1024 * 1024, message="Maximum file size is 10 MB.")
        ]
    )
    submit = SubmitField("Book Appointment")


class StatusForm(FlaskForm):
    status = SelectField(
        "Appointment Status",
        choices=[
            ("Pending", "Pending"),
            ("Confirmed", "Confirmed"),
            ("Completed", "Completed"),
            ("Cancelled", "Cancelled")
        ],
        validators=[DataRequired()]
    )
    submit = SubmitField("Update Status")
