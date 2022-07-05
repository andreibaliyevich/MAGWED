from rest_framework import serializers
from accounts.serializer_fields import UserSerializerField
from .models import Chat, Message
from .serializer_fields import MessageSerializerField


class ChatSerializer(serializers.ModelSerializer):
    """ Chat Serializer """
    members = UserSerializerField(read_only=True, many=True)
    last_message = MessageSerializerField()

    class Meta:
        model = Chat
        fields = [
            'id',
            'members',
            'last_message',
        ]


class MessageSerializer(serializers.ModelSerializer):
    """ Message Serializer """

    class Meta:
        model = Message
        fields = [
            'sender',
            'content',
            'is_viewed',
            'created_at',
        ]
