from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """ Notification Model for admin """
    list_display = (
        'id',
        'initiator',
        'recipient',
        'action',
        'viewed',
        'created_at',
    )
    readonly_fields = ('created_at',)
