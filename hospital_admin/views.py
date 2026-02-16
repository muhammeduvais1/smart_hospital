from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from smart_hospital.permissions import group_required
from doctor.models import Doctor
from patient.models import Patient
from .models import Appointment, MedicalRecord
from .forms import AppointmentForm, MedicalRecordForm


@login_required
@group_required('Admin')
def index(request):
    # Dashboard: counts and upcoming appointments
    counts = {
        'doctors': Doctor.objects.count(),
        'patients': Patient.objects.count(),
        'appointments': Appointment.objects.count(),
    }
    upcoming = Appointment.objects.order_by('scheduled_at')[:7]
    return render(request, 'hospital_admin/index.html', {'counts': counts, 'upcoming': upcoming})


@login_required
@group_required('Admin')
def appointments_list(request):
    qs = Appointment.objects.select_related('patient', 'doctor').all()
    q = request.GET.get('q')
    if q:
        qs = qs.filter(patient__first_name__icontains=q) | qs.filter(patient__last_name__icontains=q) | qs.filter(doctor__first_name__icontains=q) | qs.filter(doctor__last_name__icontains=q)
    return render(request, 'hospital_admin/appointments.html', {'appointments': qs, 'q': q})


@login_required
@group_required('Admin')
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appt = form.save(commit=False)
            # Basic availability check: ensure appointment falls within doctor's availability for that weekday
            from django.utils import timezone
            wd = appt.scheduled_at.weekday()
            avail = appt.doctor.availabilities.filter(weekday=wd)
            ok = False
            for a in avail:
                if a.start_time <= appt.scheduled_at.time() <= a.end_time:
                    ok = True
                    break
            if not ok and avail.exists():
                form.add_error('scheduled_at', 'Selected time is outside doctor availability')
            else:
                appt.save()
                form.save_m2m()
                return redirect('hospital_admin:appointments')
    else:
        form = AppointmentForm()
    return render(request, 'hospital_admin/appointment_form.html', {'form': form, 'title': 'Schedule Appointment'})


def appointments_json(request):
    qs = Appointment.objects.select_related('patient', 'doctor').all()
    data = []
    for a in qs:
        data.append({
            'id': a.pk,
            'title': f"{a.patient}",
            'start': a.scheduled_at.isoformat(),
            'doctor': str(a.doctor)
        })
    from django.http import JsonResponse
    return JsonResponse(data, safe=False)


@login_required
@group_required('Admin')
def appointment_delete(request, pk):
    appt = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appt.delete()
        return redirect('hospital_admin:appointments')
    return render(request, 'hospital_admin/confirm_delete.html', {'object': appt, 'title': 'Delete Appointment'})


@login_required
@group_required('Admin')
def medical_records_list(request):
    records = MedicalRecord.objects.select_related('patient').all()
    return render(request, 'hospital_admin/records.html', {'records': records})


@login_required
@group_required('Admin')
def record_create(request):
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('hospital_admin:records')
    else:
        form = MedicalRecordForm()
    return render(request, 'hospital_admin/record_form.html', {'form': form, 'title': 'Add Medical Record'})
