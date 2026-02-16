from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from smart_hospital.permissions import group_required
from .models import Doctor, DoctorAvailability
from .forms import DoctorForm, DoctorAvailabilityForm
from hospital_admin.models import Appointment
from django.utils import timezone


def index(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor/index.html', {'doctors': doctors})


@login_required
@group_required('Admin')
def create(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor:index')
    else:
        form = DoctorForm()
    return render(request, 'doctor/form.html', {'form': form, 'title': 'Add Doctor'})


@login_required
@group_required('Admin')
def update(request, pk):
    obj = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('doctor:index')
    else:
        form = DoctorForm(instance=obj)
    return render(request, 'doctor/form.html', {'form': form, 'title': 'Edit Doctor'})


@login_required
@group_required('Admin')
def delete(request, pk):
    obj = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        obj.delete()
        return redirect('doctor:index')
    return render(request, 'doctor/confirm_delete.html', {'object': obj, 'title': 'Delete Doctor'})


def detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    # upcoming appointments
    upcoming = Appointment.objects.filter(doctor=doctor, scheduled_at__gte=timezone.now()).order_by('scheduled_at')[:10]
    avail = doctor.availabilities.all()
    return render(request, 'doctor/detail.html', {'doctor': doctor, 'upcoming': upcoming, 'availabilities': avail})


@login_required
@group_required('Admin')
def availability_list(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    availabilities = doctor.availabilities.all()
    return render(request, 'doctor/availability_list.html', {'doctor': doctor, 'availabilities': availabilities})


@login_required
@group_required('Admin')
def availability_create(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        form = DoctorAvailabilityForm(request.POST)
        if form.is_valid():
            avail = form.save(commit=False)
            avail.doctor = doctor
            avail.save()
            return redirect('doctor:availability_list', pk=doctor.pk)
    else:
        form = DoctorAvailabilityForm()
    return render(request, 'doctor/availability_form.html', {'form': form, 'doctor': doctor, 'title': 'Add Availability'})


@login_required
@group_required('Admin')
def availability_delete(request, pk, avail_pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    avail = get_object_or_404(DoctorAvailability, pk=avail_pk, doctor=doctor)
    if request.method == 'POST':
        avail.delete()
        return redirect('doctor:availability_list', pk=doctor.pk)
    return render(request, 'doctor/confirm_delete.html', {'object': avail, 'title': 'Delete Availability'})
