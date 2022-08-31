from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
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

    def validate(self, data):
        user = self.context['request'].user
        members = data['conversation'].members.all()

        if not user in members:
            raise serializers.ValidationError({
                'conversation': _('You are not a member of the conversation.')
            })

        return data

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
    size = serializers.SerializerMethodField()

    def get_size(self, obj):
        return obj.content.size

    class Meta:
        model = ImageMessage
        fields = [
            'id',
            'content',
            'size',
        ]


class FileMessageSerializer(serializers.ModelSerializer):
    """ File Message Serializer """
    size = serializers.SerializerMethodField()

    def get_size(self, obj):
        return obj.content.size

    class Meta:
        model = FileMessage
        fields = [
            'id',
            'content',
            'size',
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
