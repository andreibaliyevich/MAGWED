from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    """ Notification Model for admin """
    list_display = (
        'id',
        'notice_type',
        'content_type',
        'object_id',
        'recipient',
        'viewed',
        'created_at',
    )
    readonly_fields = ('created_at',)


admin.site.register(Notification, NotificationAdmin)
