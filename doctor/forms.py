from django import forms
from .models import Doctor, DoctorAvailability, WEEKDAYS


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['first_name', 'last_name', 'specialty']


class DoctorAvailabilityForm(forms.ModelForm):
    class Meta:
        model = DoctorAvailability
        fields = ['weekday', 'start_time', 'end_time']
        widgets = {
            'weekday': forms.Select(choices=WEEKDAYS, attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')
        if start and end and start >= end:
            raise forms.ValidationError('End time must be after start time.')
        return cleaned_data

