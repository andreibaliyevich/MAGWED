from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Notification
from .services import send_notification


@receiver(post_save, sender=Notification)
def saved_notification(sender, instance, created, **kwargs):
    """ Send saved notification """
    if created:
        send_notification(instance, 'created')
    else:
        send_notification(instance, 'updated')


@receiver(post_delete, sender=Notification)
def deleted_notification(sender, instance, **kwargs):
    """ Send deleted notification """
    send_notification(instance, 'deleted')
