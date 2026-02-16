from django.contrib import admin
from .models import Patient, TestResult


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone', 'dob')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('dob',)


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('patient', 'test_type', 'test_name', 'test_date', 'status')
    search_fields = ('patient__first_name', 'patient__last_name', 'test_name')
    list_filter = ('test_type', 'status', 'test_date')
    readonly_fields = ('created_at', 'updated_at')
