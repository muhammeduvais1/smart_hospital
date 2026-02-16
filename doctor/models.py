from django.db import models

WEEKDAYS = [
    (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'),
    (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')
]


class Doctor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DoctorAvailability(models.Model):
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name='availabilities')
    weekday = models.IntegerField(choices=WEEKDAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['doctor', 'weekday', 'start_time']

    def __str__(self):
        return f"{self.doctor} available {self.get_weekday_display()} {self.start_time}-{self.end_time}"
