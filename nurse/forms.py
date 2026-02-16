from django import forms
from .models import Nurse


class NurseForm(forms.ModelForm):
    class Meta:
        model = Nurse
        fields = ['first_name', 'last_name']
