from rest_framework import serializers
from accounts.serializer_fields import UserSerializerField
from .choices import ConversationType
from .models import Conversation, Message
from .serializer_fields import (
    GroupConversationSerializerField,
    MessageSerializerField,
)


class ConversationSerializer(serializers.ModelSerializer):
    """ Conversation Serializer """
    details = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    def get_details(self, obj):
        request = self.context['request']

        if obj.convo_type == ConversationType.DIALOG:
            return UserSerializerField(
                obj.members.exclude(id=request.user.id).first(),
                context={'request': request},
            ).data
        elif obj.convo_type == ConversationType.GROUP:
            return GroupConversationSerializerField(
                obj.group_details,
                context={'request': request},
            ).data
        else:
            return None

    def get_last_message(self, obj):
        return MessageSerializerField(
            obj.messages.order_by('created_at').last(),
        ).data

    class Meta:
        model = Conversation
        fields = [
            'id',
            'convo_type',
            'members',
            'details',
            'last_message',
        ]


class MessageSerializer(serializers.ModelSerializer):
    """ Message Serializer """
    sender = UserSerializerField(read_only=True)

    class Meta:
        model = Message
        fields = [
            'sender',
            'content',
            'is_viewed',
            'created_at',
        ]
