from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from smart_hospital.permissions import group_required
from .models import Patient, TestResult
from .forms import PatientForm, TestResultForm
from hospital_admin.models import MedicalRecord, Appointment



def index(request):
    patients = Patient.objects.all()
    return render(request, 'patient/index.html', {'patients': patients})


@login_required
@group_required('Admin')
def create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient:index')
    else:
        form = PatientForm()
    return render(request, 'patient/form.html', {'form': form, 'title': 'Add Patient'})


@login_required
@group_required('Admin')
def update(request, pk):
    obj = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('patient:index')
    else:
        form = PatientForm(instance=obj)
    return render(request, 'patient/form.html', {'form': form, 'title': 'Edit Patient'})


@login_required
@group_required('Admin')
def delete(request, pk):
    obj = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('patient:index')
    return render(request, 'patient/confirm_delete.html', {'object': obj, 'title': 'Delete Patient'})


@login_required
def detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    records = MedicalRecord.objects.filter(patient=patient).order_by('-created_at')
    appointments = Appointment.objects.filter(patient=patient).order_by('-scheduled_at')
    test_results = TestResult.objects.filter(patient=patient).order_by('-test_date')
    return render(request, 'patient/detail.html', {
        'patient': patient,
        'records': records,
        'appointments': appointments,
        'test_results': test_results,
    })


@login_required
@group_required('Admin')
def add_test_result(request, pk):
    """Add a test result for a patient"""
    patient = get_object_or_404(Patient, pk=pk)
    
    if request.method == 'POST':
        form = TestResultForm(request.POST, request.FILES)
        if form.is_valid():
            test_result = form.save(commit=False)
            test_result.patient = patient
            test_result.save()
            return redirect('patient:detail', pk=pk)
    else:
        form = TestResultForm()
    
    return render(request, 'patient/test_result_form.html', {
        'form': form,
        'patient': patient,
        'title': f'Add Test Result for {patient.first_name} {patient.last_name}'
    })


@login_required
@group_required('Admin')
def edit_test_result(request, pk, result_id):
    """Edit a test result"""
    patient = get_object_or_404(Patient, pk=pk)
    test_result = get_object_or_404(TestResult, id=result_id, patient=patient)
    
    if request.method == 'POST':
        form = TestResultForm(request.POST, request.FILES, instance=test_result)
        if form.is_valid():
            form.save()
            return redirect('patient:detail', pk=pk)
    else:
        form = TestResultForm(instance=test_result)
    
    return render(request, 'patient/test_result_form.html', {
        'form': form,
        'patient': patient,
        'test_result': test_result,
        'title': f'Edit Test Result for {patient.first_name} {patient.last_name}'
    })


@login_required
@group_required('Admin')
def delete_test_result(request, pk, result_id):
    """Delete a test result"""
    patient = get_object_or_404(Patient, pk=pk)
    test_result = get_object_or_404(TestResult, id=result_id, patient=patient)
    
    if request.method == 'POST':
        test_result.delete()
        return redirect('patient:detail', pk=pk)
    
    return render(request, 'patient/test_result_confirm_delete.html', {
        'patient': patient,
        'test_result': test_result,
    })


@login_required
def test_results_list(request, pk):
    """View all test results for a patient"""
    patient = get_object_or_404(Patient, pk=pk)
    test_results = TestResult.objects.filter(patient=patient).order_by('-test_date')
    
    return render(request, 'patient/test_results_list.html', {
        'patient': patient,
        'test_results': test_results,
    })

