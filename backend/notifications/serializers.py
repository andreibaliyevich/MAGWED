from rest_framework import serializers
from .models import Notification
from .serializer_fields import NotificationObjectRelatedField

class NotificationListSerializer(serializers.ModelSerializer):
    """ Notification List Serializer """
    content_object = NotificationObjectRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'notice_type',
            'content_object',
            'viewed',
            'created_at',
        ]
