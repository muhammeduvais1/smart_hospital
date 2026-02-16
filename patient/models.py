from django.db import models


class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField(null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TestResult(models.Model):
    """Model to store patient test results"""
    TEST_TYPE_CHOICES = [
        ('blood', 'Blood Test'),
        ('xray', 'X-Ray'),
        ('ultrasound', 'Ultrasound'),
        ('ct_scan', 'CT Scan'),
        ('mri', 'MRI'),
        ('ecg', 'ECG'),
        ('urinalysis', 'Urinalysis'),
        ('covid', 'COVID-19 Test'),
        ('diabetes', 'Diabetes Test'),
        ('thyroid', 'Thyroid Test'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='test_results')
    test_type = models.CharField(max_length=50, choices=TEST_TYPE_CHOICES)
    test_name = models.CharField(max_length=255)
    test_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    result_value = models.CharField(max_length=255, blank=True, null=True)
    normal_range = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='test_results/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-test_date']

    def __str__(self):
        return f"{self.patient.first_name} - {self.test_name} ({self.test_date})"

