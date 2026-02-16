from django import forms
from .models import Appointment, MedicalRecord


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'scheduled_at', 'reason']
        widgets = {
            'scheduled_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            'reason': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Check-up, Follow-up visit'}),
        }


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'notes']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-select'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Enter clinical notes here...'}),
        }

