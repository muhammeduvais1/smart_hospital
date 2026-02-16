from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Appointment
from .notifications import NotificationService


@receiver(post_save, sender=Appointment)
def appointment_created(sender, instance, created, **kwargs):
    if created:
        NotificationService.send_appointment_created(instance)


@receiver(post_delete, sender=Appointment)
def appointment_deleted(sender, instance, **kwargs):
    NotificationService.send_appointment_cancelled(instance)
