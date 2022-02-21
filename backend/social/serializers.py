from rest_framework import serializers
from .models import Notification, Comment
from .serializer_fields import ContentObjectRelatedField


class NotificationListSerializer(serializers.ModelSerializer):
    """ Notification List Serializer """
    content_object = ContentObjectRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'content_object',
            'viewed',
            'created_at',
        ]


class CommentCreateSerializer(serializers.ModelSerializer):
    """ Comment Create Serializer """

    class Meta:
        model = Comment
        fields = [
            'content',
        ]
