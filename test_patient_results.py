#!/usr/bin/env python
"""
Test script for patient test results functionality
"""
import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_hospital.settings')
django.setup()

from patient.models import Patient, TestResult

print("=" * 70)
print("PATIENT TEST RESULTS FEATURE TEST")
print("=" * 70)

try:
    # Test 1: Get a patient
    print("\n1. Retrieving patients...")
    patients = Patient.objects.all()[:1]
    if not patients:
        print("   ✗ No patients found in database")
        print("   - Create a patient first via admin or patient creation page")
    else:
        patient = patients[0]
        print(f"   ✓ Found patient: {patient.first_name} {patient.last_name}")
        
        # Test 2: Create test results
        print("\n2. Creating sample test results...")
        
        test_data = [
            {
                'test_type': 'blood',
                'test_name': 'Complete Blood Count (CBC)',
                'test_date': date.today() - timedelta(days=5),
                'status': 'completed',
                'result_value': '4.5 million/mcL',
                'normal_range': '4.0-5.5 million/mcL',
                'notes': 'Healthy red blood cell count'
            },
            {
                'test_type': 'diabetes',
                'test_name': 'Fasting Blood Glucose',
                'test_date': date.today() - timedelta(days=3),
                'status': 'completed',
                'result_value': '95 mg/dL',
                'normal_range': '70-100 mg/dL',
                'notes': 'Normal fasting glucose level'
            },
            {
                'test_type': 'thyroid',
                'test_name': 'TSH Level',
                'test_date': date.today(),
                'status': 'pending',
                'result_value': None,
                'normal_range': '0.4-4.0 mIU/L',
                'notes': 'Results pending from lab'
            },
        ]
        
        created_tests = []
        for test_data_item in test_data:
            test = TestResult.objects.create(
                patient=patient,
                **test_data_item
            )
            created_tests.append(test)
            print(f"   ✓ Created: {test.test_name} ({test.status})")
        
        # Test 3: Query test results
        print("\n3. Querying test results...")
        all_tests = TestResult.objects.filter(patient=patient)
        print(f"   ✓ Total tests for patient: {all_tests.count()}")
        
        completed_tests = TestResult.objects.filter(patient=patient, status='completed')
        print(f"   ✓ Completed tests: {completed_tests.count()}")
        
        pending_tests = TestResult.objects.filter(patient=patient, status='pending')
        print(f"   ✓ Pending tests: {pending_tests.count()}")
        
        # Test 4: Display test details
        print("\n4. Test Results Details:")
        for test in all_tests.order_by('-test_date'):
            print(f"\n   Test: {test.test_name}")
            print(f"   - Type: {test.get_test_type_display()}")
            print(f"   - Date: {test.test_date.strftime('%d %B %Y')}")
            print(f"   - Status: {test.get_status_display().upper()}")
            if test.result_value:
                print(f"   - Result: {test.result_value}")
                print(f"   - Normal Range: {test.normal_range}")
            if test.notes:
                print(f"   - Notes: {test.notes}")
        
        # Test 5: Update test result
        print("\n5. Updating test result...")
        if created_tests:
            test_to_update = created_tests[2]  # The pending test
            test_to_update.status = 'completed'
            test_to_update.result_value = '2.5 mIU/L'
            test_to_update.save()
            print(f"   ✓ Updated {test_to_update.test_name} to completed")
            print(f"   - New result: {test_to_update.result_value}")
        
        # Test 6: Delete test result
        print("\n6. Testing deletion...")
        if created_tests:
            test_to_delete = created_tests[0]
            test_id = test_to_delete.id
            test_name = test_to_delete.test_name
            test_to_delete.delete()
            print(f"   ✓ Deleted: {test_name}")
        
        # Test 7: Final count
        print("\n7. Final test count...")
        final_count = TestResult.objects.filter(patient=patient).count()
        print(f"   ✓ Remaining tests: {final_count}")
        
        print("\n" + "=" * 70)
        print("TEST RESULTS FEATURE TEST COMPLETED SUCCESSFULLY")
        print("=" * 70)
        print("\nTo access the feature via web interface:")
        print(f"1. Log in to http://localhost:8000/accounts/login/")
        print(f"2. Go to Patients → Select '{patient.first_name} {patient.last_name}'")
        print(f"3. Click 'Test Results' tab to view and manage tests")
        print(f"4. Click '+ Add Test Result' to create new tests")
        print("\n" + "=" * 70)

except Exception as e:
    print(f"\n✗ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
