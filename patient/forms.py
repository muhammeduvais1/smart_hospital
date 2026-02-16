from django import forms
from .models import Patient, TestResult


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'dob', 'email', 'phone']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 123-4567'}),
        }


class TestResultForm(forms.ModelForm):
    class Meta:
        model = TestResult
        fields = ['test_type', 'test_name', 'test_date', 'status', 'result_value', 'normal_range', 'notes', 'file']
        widgets = {
            'test_type': forms.Select(attrs={'class': 'form-control'}),
            'test_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Complete Blood Count (CBC)'
            }),
            'test_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'result_value': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 120 mg/dL'
            }),
            'normal_range': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 70-100 mg/dL'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Additional notes or observations...'
            }),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
