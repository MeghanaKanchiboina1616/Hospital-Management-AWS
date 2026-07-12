# 🏥 Cloud-Based Hospital Management System

A cloud-based Hospital Management System developed using **Flask** and deployed on **AWS Elastic Beanstalk**. The application enables patients to register, log in, book appointments, upload medical reports, and manage their healthcare information through a secure and user-friendly web interface.

---

## 📌 Project Overview

GM Hospital Portal is a full-stack web application designed to simplify hospital management by digitizing patient services. The application integrates multiple AWS cloud services to provide scalable, reliable, and secure healthcare data management.

---

## ✨ Features

### 👤 Patient Module
- Patient Registration
- Secure Login & Logout
- Profile Management
- Upload Medical Reports
- View Uploaded Reports
- Book Doctor Appointments

### 👨‍⚕️ Doctor Module
- View Patient Appointments
- Manage Appointment Requests

### ☁️ Cloud Integration
- Medical reports stored securely in Amazon S3
- Patient records stored in Amazon RDS PostgreSQL
- Application deployed using AWS Elastic Beanstalk
- Application logs monitored using Amazon CloudWatch

---

# 🏗️ System Architecture

```
                    User
                     │
                     ▼
          AWS Elastic Beanstalk
             (Flask Application)
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
 Amazon RDS PostgreSQL       Amazon S3
(Patient & Appointment DB)  (Medical Reports)

                     │
                     ▼
             Amazon CloudWatch
              (Application Logs)
```

---

# 🚀 AWS Services Used

| Service | Purpose |
|----------|----------|
| Amazon Elastic Beanstalk | Application Deployment |
| Amazon RDS (PostgreSQL) | Database |
| Amazon S3 | Medical Report Storage |
| Amazon CloudWatch | Monitoring & Logging |
| IAM Roles | Secure AWS Access |

---

# 🛠️ Tech Stack

### Frontend
- HTML5
- CSS3
- Bootstrap
- JavaScript

### Backend
- Python
- Flask
- SQLAlchemy
- Flask-Migrate
- Flask-Login
- WTForms

### Database
- PostgreSQL

### Cloud
- AWS Elastic Beanstalk
- Amazon RDS
- Amazon S3
- Amazon CloudWatch

### Version Control
- Git
- GitHub

---

# 📂 Project Structure

```
GM-Hospital-Portal/
│
├── app.py
├── config.py
├── models.py
├── requirements.txt
├── Procfile
├── runtime.txt
├── .gitignore
│
├── templates/
│
├── static/
│
├── uploads/
│
├── migrations/
│
└── README.md
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/MeghanaKanchiboina1616/Hospital-Management-AWS.git

cd GM-Hospital-Portal
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate environment

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a **.env** file.

```env
DATABASE_URL=postgresql://username:password@host:5432/database_name

AWS_REGION=us-east-1

S3_BUCKET=your-bucket-name

SECRET_KEY=your-secret-key
```

---

## Run Database Migrations

```bash
flask db upgrade
```

---

## Run Application

```bash
python app.py
```

Application runs on

```
http://127.0.0.1:5000
```

---

# ☁️ Deployment

The application is deployed using **AWS Elastic Beanstalk**.

Deployment includes:

- Flask Application
- Amazon RDS PostgreSQL
- Amazon S3 Storage
- IAM Roles
- CloudWatch Logs

---

# 📸 Application Workflow

1. Patient Registration
2. Secure Login
3. Book Appointment
4. Upload Medical Report
5. Report Stored in Amazon S3
6. Patient Data Stored in Amazon RDS
7. Application Hosted on Elastic Beanstalk

---

# 🔒 Security Features

- Password Authentication
- Environment Variables
- AWS IAM Roles
- Secure Amazon S3 Storage
- PostgreSQL Database
- Server-side Validation

---

# 📈 Future Enhancements

- Admin Dashboard
- Email Notifications
- Online Payment Gateway
- Prescription Management
- AI-based Disease Prediction
- SMS Appointment Reminders

---

# 📋 Requirements

- Python 3.12+
- PostgreSQL
- AWS Account
- Amazon S3 Bucket
- Amazon RDS PostgreSQL
- Elastic Beanstalk Environment

---

# 👩‍💻 Author
**Ghanta Sri Kameshu**

B.Tech Computer Science Engineering (AI & ML)
VVIT, Andhra Pradesh

BBA
KL Deemed to be University

**Meghana Kanchiboina**

B.Tech Computer Science Engineering (AI & ML)

VVIT, Andhra Pradesh

### Skills

- Python
- Flask
- PostgreSQL
- AWS
- SQLAlchemy
- Git
- HTML
- CSS
- JavaScript

---

# ⭐ Acknowledgements

- AWS
- Flask
- PostgreSQL
- SQLAlchemy
- Bootstrap

---

# 📄 License

This project is developed for educational and internship purposes.
