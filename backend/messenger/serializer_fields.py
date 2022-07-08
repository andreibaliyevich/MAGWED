from rest_framework import serializers
from .models import GroupConversation, Message


class GroupConversationSerializerField(serializers.ModelSerializer):
    """ GroupConversation Serializer Field """

    class Meta:
        model = GroupConversation
        fields = [
            'owner',
            'name',
            'image',
        ]


class MessageSerializerField(serializers.ModelSerializer):
    """ Message Serializer Field """

    class Meta:
        model = Message
        fields = [
            'content',
            'is_viewed',
            'created_at',
        ]
