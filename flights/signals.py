from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Flight
from notifications.tasks import send_flight_delay_notification

@receiver(pre_save, sender=Flight)
def flight_status_change_handler(sender, instance, **kwargs):
  if not instance.pk:
    return 

  old = Flight.objects.get(pk=instance.pk)
  if old.status != 'delayed' and instance.status == 'delayed':
    send_flight_delay_notification.delay(instance.pk, instance.flight_number)
