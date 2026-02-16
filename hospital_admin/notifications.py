from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import logging

logger = logging.getLogger(__name__)


class NotificationService:
    """Send appointment notifications via email and SMS."""

    @staticmethod
    def send_appointment_created(appointment):
        """Send notification when appointment is created."""
        patient = appointment.patient
        doctor = appointment.doctor
        
        # Email notification
        if patient.email:
            try:
                subject = f"Appointment Confirmed: {doctor.first_name} {doctor.last_name}"
                context = {
                    'patient_name': patient.first_name,
                    'doctor_name': f"{doctor.first_name} {doctor.last_name}",
                    'specialty': doctor.specialty,
                    'appointment_date': appointment.scheduled_at.strftime("%B %d, %Y"),
                    'appointment_time': appointment.scheduled_at.strftime("%I:%M %p"),
                    'reason': appointment.reason or "General appointment",
                }
                html_message = render_to_string('email/appointment_created.html', context)
                send_mail(
                    subject,
                    f"Your appointment with {doctor.first_name} {doctor.last_name} is scheduled for {appointment.scheduled_at}",
                    settings.DEFAULT_FROM_EMAIL,
                    [patient.email],
                    html_message=html_message,
                    fail_silently=False
                )
                logger.info(f"Email sent to {patient.email} for appointment {appointment.pk}")
            except Exception as e:
                logger.error(f"Failed to send email to {patient.email}: {str(e)}")

        # SMS notification
        if patient.phone:
            NotificationService.send_sms(
                patient.phone,
                f"Hi {patient.first_name}, your appointment with Dr. {doctor.last_name} is confirmed for {appointment.scheduled_at.strftime('%b %d at %I:%M %p')}."
            )

        # Admin notification
        admin_subject = f"New Appointment: {patient.first_name} {patient.last_name} with {doctor.first_name} {doctor.last_name}"
        admin_message = f"Appointment scheduled for {appointment.scheduled_at}\nReason: {appointment.reason or 'N/A'}"
        send_mail(
            admin_subject,
            admin_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False
        )
        logger.info(f"Admin notification sent for appointment {appointment.pk}")

    @staticmethod
    def send_appointment_cancelled(appointment):
        """Send notification when appointment is cancelled."""
        patient = appointment.patient
        doctor = appointment.doctor
        
        # Email notification
        if patient.email:
            try:
                subject = f"Appointment Cancelled: {doctor.first_name} {doctor.last_name}"
                context = {
                    'patient_name': patient.first_name,
                    'doctor_name': f"{doctor.first_name} {doctor.last_name}",
                    'appointment_date': appointment.scheduled_at.strftime("%B %d, %Y"),
                    'appointment_time': appointment.scheduled_at.strftime("%I:%M %p"),
                }
                html_message = render_to_string('email/appointment_cancelled.html', context)
                send_mail(
                    subject,
                    f"Your appointment with {doctor.first_name} {doctor.last_name} on {appointment.scheduled_at} has been cancelled.",
                    settings.DEFAULT_FROM_EMAIL,
                    [patient.email],
                    html_message=html_message,
                    fail_silently=False
                )
                logger.info(f"Cancellation email sent to {patient.email}")
            except Exception as e:
                logger.error(f"Failed to send cancellation email: {str(e)}")

        # SMS notification
        if patient.phone:
            NotificationService.send_sms(
                patient.phone,
                f"Hi {patient.first_name}, your appointment with Dr. {doctor.last_name} on {appointment.scheduled_at.strftime('%b %d')} has been cancelled."
            )

    @staticmethod
    def send_sms(phone_number, message):
        """
        Send SMS notification.
        
        Stub implementation - replace with real SMS provider (Twilio, AWS SNS, etc.)
        """
        # In production, integrate with SMS provider:
        # from twilio.rest import Client
        # client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        # client.messages.create(to=phone_number, from_=TWILIO_PHONE, body=message)
        
        logger.info(f"[SMS STUB] To: {phone_number} | Message: {message}")
        print(f"\n{'='*60}")
        print(f"SMS NOTIFICATION")
        print(f"{'='*60}")
        print(f"To: {phone_number}")
        print(f"Message: {message}")
        print(f"{'='*60}\n")
