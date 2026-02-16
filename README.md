# Smart Hospital (Django)

![Release](https://img.shields.io/github/v/release/muhammeduvais1/smart_hospital?style=flat-square)

A complete smart hospital management system with doctors, patients, nurses, appointments, medical records, role-based access, and doctor availability scheduling.

## Features

- **Multi-role system**: Admin, Doctor, Nurse, Patient groups
- **Doctor Management**: CRUD + schedule weekly availability
- **Patient Management**: CRUD + view medical records & appointments
- **Nurse Management**: CRUD
- **Appointments**: Schedule, search, calendar view, availability validation
- **Medical Records**: Create and view patient medical history
- **Role-Based Access Control**: Login required, admin-only features protected
- **Notifications**: Email (console backend) and SMS (stub) on appointment changes
- **Modern UI**: Bootstrap 5 + animations

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run migrations:**
```bash
python manage.py migrate
```

3. **Verify system:**
```bash
python test_system.py
```

4. **Start dev server:**
```bash
python manage.py runserver
```

5. **Login:**
- URL: http://127.0.0.1:8000/
- Username: `admin`
- Password: `AdminPass123!`

## Admin Workflows

### Add Doctor Availability
1. Go to **Doctors** → click **Schedule** next to any doctor
2. Click **+ Add Time Slot**
3. Select day, start time, end time → **Save Time Slot**
4. Appointments must fit within these scheduled times

### Schedule Appointment
1. Go to **Appointments** → **+ Schedule Appointment**
2. Select patient, doctor, date/time, reason
3. System validates time against doctor's availability
4. Triggers notification email/SMS (check console)

### View Patient Medical History
1. Go to **Patients** → click patient name
2. See all appointments and medical records in one place

### Add Medical Record
1. Go to **Records** → **+ Add Record**
2. Select patient, enter notes → **Save**

## Settings

- **Email**: Console backend (dev mode, prints to terminal)
- **SMS**: Stub backend (prints to terminal)
- **Database**: SQLite (db.sqlite3)
- **Login required**: Yes (all non-list views)
- **Admin-only features**: Create/edit/delete doctors, patients, nurses, manage availability, schedule appointments, view records

## Database

All migrations are pre-applied. Models include:
- `doctor.Doctor` + `doctor.DoctorAvailability`
- `patient.Patient`
- `nurse.Nurse`
- `hospital_admin.Appointment` + `hospital_admin.MedicalRecord`
- Django `User` + `Group` (4 groups: Admin, Doctor, Nurse, Patient)

Run `python test_system.py` to verify all data.

## URLs

- Dashboard: `/`
- Doctors: `/doctors/`
- Patients: `/patients/`
- Nurses: `/nurses/`
- Appointments: `/appointments/`
- Appointments Calendar: `/calendar/`
- Medical Records: `/records/`
- Doctor Availability: `/doctors/<id>/availability/`
- Admin Portal: `/admin/`
- Login: `/accounts/login/`

## Troubleshooting

**"'hospital_tags' is not registered"** → Restart server after adding to `INSTALLED_APPS`.

**Appointments form shows error** → Doctor must have availability slots for that day/time.

**Migrations not applied** → Run `python manage.py migrate`.

**Missing data** → Run `python create_sample_data.py` and `python create_roles.py`.

---

Built with Django 4.2+, Bootstrap 5, and modern best practices.

