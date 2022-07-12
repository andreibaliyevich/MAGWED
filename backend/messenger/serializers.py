from rest_framework import serializers
from accounts.serializer_fields import UserSerializerField
from .choices import ConversationType, MessageType
from .models import (
    Conversation,
    Message,
    TextMessage,
    ImageMessage,
    FileMessage,
)
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


class MessageReadSerializer(serializers.ModelSerializer):
    """ Message Read Serializer """
    sender = UserSerializerField(read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'created_at',
            'is_viewed',
            'get_content',
        ]


class MessageWriteSerializer(serializers.ModelSerializer):
    """ Message Write Serializer """
    content = serializers.CharField(write_only=True)

    def create(self, validated_data):
        msg = Message.objects.create(
            conversation=validated_data['conversation'],
            sender=validated_data['sender'],
            msg_type=MessageType.TEXT,
        )
        TextMessage.objects.create(
            message=msg,
            content=validated_data['content']
        )
        return msg

    class Meta:
        model = Message
        fields = [
            'conversation',
            'sender',
            'content',
        ]
