from rest_framework import serializers
from accounts.serializers import UserShortReadSerializer
from .models import Notification
from .serializer_fields import NotificationObjectRelatedField

class NotificationListSerializer(serializers.ModelSerializer):
    """ Notification List Serializer """
    initiator = UserShortReadSerializer(read_only=True)
    content_object = NotificationObjectRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'initiator',
            'action',
            'content_object',
            'viewed',
            'created_at',
        ]
