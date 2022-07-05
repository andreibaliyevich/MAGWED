from rest_framework import serializers
from .models import Message


class MessageSerializerField(serializers.ModelSerializer):
    """ Message Serializer Field """

    class Meta:
        model = Message
        fields = [
            'content',
            'is_viewed',
            'created_at',
        ]
