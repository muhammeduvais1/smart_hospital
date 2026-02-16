import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_hospital.settings')
django.setup()

from doctor.models import Doctor
from patient.models import Patient
from nurse.models import Nurse

if __name__ == '__main__':
    Doctor.objects.all().delete()
    Patient.objects.all().delete()
    Nurse.objects.all().delete()

    Doctor.objects.create(first_name='Alice', last_name='Smith', specialty='Cardiology')
    Doctor.objects.create(first_name='Bob', last_name='Jones', specialty='Neurology')

    Patient.objects.create(first_name='John', last_name='Doe')
    Patient.objects.create(first_name='Jane', last_name='Roe')

    Nurse.objects.create(first_name='Nancy', last_name='Drew')

    print('Sample data created.')
