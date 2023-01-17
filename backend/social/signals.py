from django.db.models import Avg, Value
from django.db.models.functions import Coalesce
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review


@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_organizer_rating(sender, **kwargs):
    """ Update rating of organizer """
    organizer = kwargs['instance'].organizer
    organizer_rating = organizer.organizer_reviews.aggregate(
        total_rating=Coalesce(Avg('rating'), Value(0.0)))
    organizer.rating = organizer_rating['total_rating']
    organizer.save(update_fields=['rating'])
