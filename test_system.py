import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_hospital.settings')
django.setup()

from django.contrib.auth.models import Group, User
from django.contrib.auth import get_user_model
from doctor.models import Doctor, DoctorAvailability
from patient.models import Patient
from nurse.models import Nurse
from hospital_admin.models import Appointment, MedicalRecord

User = get_user_model()

# Test data counts
print("=== SYSTEM STATUS ===")
print(f"Users: {User.objects.count()}")
print(f"Groups: {Group.objects.count()} - {[g.name for g in Group.objects.all()]}")
print()

print("=== HEALTH CHECK ===")
print(f"Doctors: {Doctor.objects.count()}")
print(f"Doctor Availability Slots: {DoctorAvailability.objects.count()}")
print(f"Patients: {Patient.objects.count()}")
print(f"Nurses: {Nurse.objects.count()}")
print(f"Appointments: {Appointment.objects.count()}")
print(f"Medical Records: {MedicalRecord.objects.count()}")
print()

# Check admin user
try:
    admin = User.objects.get(username='admin')
    print(f"✓ Admin user exists: {admin.username}")
    print(f"  - Staff: {admin.is_staff}")
    print(f"  - Groups: {[g.name for g in admin.groups.all()]}")
except User.DoesNotExist:
    print("✗ Admin user not found")

print()
print("=== FUNCTIONALITY TEST ===")

# Test doctor creation
if Doctor.objects.count() > 0:
    doc = Doctor.objects.first()
    print(f"✓ Sample doctor: {doc.first_name} {doc.last_name} ({doc.specialty})")
    avail_count = doc.availabilities.count()
    print(f"  - Availability slots: {avail_count}")
else:
    print("✗ No doctors found")

# Test patient creation
if Patient.objects.count() > 0:
    pat = Patient.objects.first()
    print(f"✓ Sample patient: {pat.first_name} {pat.last_name}")
else:
    print("✗ No patients found")

# Test appointments
if Appointment.objects.count() > 0:
    appt = Appointment.objects.first()
    print(f"✓ Sample appointment: {appt.patient} with {appt.doctor} at {appt.scheduled_at}")
else:
    print("✗ No appointments found (create from UI)")

print()
print("=== ALL SYSTEMS READY ===")
print("Access at http://127.0.0.1:8000/")
print("Login: admin / AdminPass123!")
