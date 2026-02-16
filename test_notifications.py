#!/usr/bin/env python
"""
Test notification system for appointments.
Usage: python test_notifications.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_hospital.settings')
django.setup()

from doctor.models import Doctor
from patient.models import Patient
from hospital_admin.models import Appointment
from datetime import datetime, timedelta

print("=== TESTING APPOINTMENT NOTIFICATIONS ===\n")

# Get sample doctor and patient
try:
    doc = Doctor.objects.first()
    if not doc:
        print("✗ No doctors found. Please add a doctor first.")
        exit(1)
    
    # Get or create a patient with email/phone
    pat, created = Patient.objects.get_or_create(
        first_name='Test',
        last_name='Patient',
        defaults={
            'email': 'patient@example.com',
            'phone': '+1 (555) 123-4567'
        }
    )
    
    if created:
        print(f"✓ Created test patient: {pat} with email={pat.email}, phone={pat.phone}")
    else:
        print(f"✓ Using existing patient: {pat} with email={pat.email}, phone={pat.phone}")
    
    # Create appointment (this triggers signals)
    future_time = datetime.now() + timedelta(days=7)
    appt = Appointment.objects.create(
        patient=pat,
        doctor=doc,
        scheduled_at=future_time,
        reason='Test appointment for notification testing'
    )
    
    print(f"✓ Created appointment #{appt.pk}")
    print(f"  - Patient: {appt.patient}")
    print(f"  - Doctor: {appt.doctor}")
    print(f"  - Date/Time: {appt.scheduled_at}")
    print("\n✓ Notifications should have been sent above (email + SMS)")
    print("\nTo see real email in console output, check the Django development server logs.")
    
except Exception as e:
    print(f"✗ Error: {str(e)}")
    import traceback
    traceback.print_exc()
