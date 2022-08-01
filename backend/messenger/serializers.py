from rest_framework import serializers
from accounts.serializers import UserShortReadSerializer
from .choices import ConversationType, MessageType
from .models import (
    Conversation,
    GroupConversation,
    Message,
    TextMessage,
    ImageMessage,
    FileMessage,
)


class MessageCreateSerializer(serializers.ModelSerializer):
    """ Message Create Serializer """

    class Meta:
        model = Message
        fields = ['conversation']


class TextMessageSerializer(serializers.ModelSerializer):
    """ Text Message Serializer """

    class Meta:
        model = TextMessage
        fields = ['content']


class ImageMessageSerializer(serializers.ModelSerializer):
    """ Image Message Serializer """

    class Meta:
        model = ImageMessage
        fields = [
            'id',
            'content',
        ]


class FileMessageSerializer(serializers.ModelSerializer):
    """ File Message Serializer """

    class Meta:
        model = FileMessage
        fields = [
            'id',
            'content',
        ]


class MessageFullReadSerializer(serializers.ModelSerializer):
    """ Message Full Read Serializer """
    sender = UserShortReadSerializer(read_only=True)
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        if obj.msg_type == MessageType.TEXT:
            return TextMessageSerializer(obj.text).data['content']
        elif obj.msg_type == MessageType.IMAGES:
            return ImageMessageSerializer(obj.images.all(), many=True).data
        elif obj.msg_type == MessageType.FILES:
            return FileMessageSerializer(obj.files.all(), many=True).data
        else:
            return None

    class Meta:
        model = Message
        fields = [
            'id',
            'sender',
            'msg_type',
            'created_at',
            'is_viewed',
            'content',
        ]


class MessageShortReadSerializer(serializers.ModelSerializer):
    """ Message Short Read Serializer """
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        if obj.msg_type == MessageType.TEXT:
            return TextMessageSerializer(obj.text).data['content']
        elif obj.msg_type == MessageType.IMAGES:
            return ImageMessageSerializer(obj.images.all(), many=True).data
        elif obj.msg_type == MessageType.FILES:
            return FileMessageSerializer(obj.files.all(), many=True).data
        else:
            return None

    class Meta:
        model = Message
        fields = [
            'msg_type',
            'is_viewed',
            'created_at',
            'content',
        ]


class GroupConversationSerializer(serializers.ModelSerializer):
    """ GroupConversation Serializer """

    class Meta:
        model = GroupConversation
        fields = [
            'owner',
            'name',
            'image',
        ]


class ConversationSerializer(serializers.ModelSerializer):
    """ Conversation Serializer """
    details = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    def get_details(self, obj):
        request = self.context['request']

        if obj.convo_type == ConversationType.DIALOG:
            return UserShortReadSerializer(
                obj.members.exclude(id=request.user.id).first(),
                context={'request': request},
            ).data
        elif obj.convo_type == ConversationType.GROUP:
            return GroupConversationSerializer(
                obj.group_details,
                context={'request': request},
            ).data
        else:
            return None

    def get_last_message(self, obj):
        return MessageShortReadSerializer(
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
