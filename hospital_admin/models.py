from django.db import models
from django.conf import settings
from patient.models import Patient
from doctor.models import Doctor


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
    scheduled_at = models.DateTimeField()
    reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['scheduled_at']

    def __str__(self):
        return f"{self.patient} with {self.doctor} at {self.scheduled_at}"


class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Record for {self.patient} ({self.created_at.date()})"
