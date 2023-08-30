from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from accounts.serializers import (
    UserBriefReadSerializer,
    UserShortReadSerializer,
)
from .choices import ChatType, MessageType
from .models import (
    Chat,
    GroupChat,
    Message,
    TextMessage,
    ImageMessage,
    FileMessage,
)


class MessageCreateSerializer(serializers.ModelSerializer):
    """ Message Create Serializer """

    def validate(self, data):
        user = self.context['request'].user
        members = data['chat'].members.all()

        if not user in members:
            raise serializers.ValidationError({
                'chat': _('You are not a member of the chat.')})

        return data

    class Meta:
        model = Message
        fields = ['chat']


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
            'uuid',
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
            'uuid',
            'content',
            'size',
        ]


class MessageFullReadSerializer(serializers.ModelSerializer):
    """ Message Full Read Serializer """
    sender = UserBriefReadSerializer(read_only=True)
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        if obj.msg_type == MessageType.TEXT:
            return TextMessageSerializer(obj.text).data['content']

        if obj.msg_type == MessageType.IMAGES:
            return ImageMessageSerializer(
                obj.images.all(),
                many=True,
                context=self.context,
            ).data

        if obj.msg_type == MessageType.FILES:
            return FileMessageSerializer(
                obj.files.all(),
                many=True,
                context=self.context,
            ).data

        return None

    class Meta:
        model = Message
        fields = [
            'uuid',
            'sender',
            'msg_type',
            'created_at',
            'viewed',
            'content',
        ]


class MessageShortReadSerializer(serializers.ModelSerializer):
    """ Message Short Read Serializer """
    content = serializers.SerializerMethodField()

    def get_content(self, obj):
        if obj.msg_type == MessageType.TEXT:
            return TextMessageSerializer(obj.text).data['content']

        if obj.msg_type == MessageType.IMAGES:
            return obj.images.all().count()

        if obj.msg_type == MessageType.FILES:
            return obj.files.all().count()

        return None

    class Meta:
        model = Message
        fields = [
            'msg_type',
            'viewed',
            'created_at',
            'content',
        ]


class GroupChatListSerializer(serializers.ModelSerializer):
    """ Group Chat List Serializer """

    class Meta:
        model = GroupChat
        fields = [
            'name',
            'image',
        ]


class GroupChatRetrieveSerializer(serializers.ModelSerializer):
    """ Group Chat Retrieve Serializer """

    class Meta:
        model = GroupChat
        fields = [
            'owner',
            'name',
            'image',
        ]


class ChatListSerializer(serializers.ModelSerializer):
    """ Chat List Serializer """
    details = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    def get_details(self, obj):
        request = self.context['request']

        if obj.chat_type == ChatType.DIALOG:
            return UserBriefReadSerializer(
                obj.members.exclude(uuid=request.user.uuid).first(),
                context={'request': request},
            ).data

        if obj.chat_type == ChatType.GROUP:
            return GroupChatListSerializer(
                obj.group_details,
                context={'request': request},
            ).data

        return None

    def get_last_message(self, obj):
        return MessageShortReadSerializer(
            obj.messages.order_by('created_at').last(),
        ).data

    class Meta:
        model = Chat
        fields = [
            'uuid',
            'chat_type',
            'members',
            'details',
            'last_message',
        ]


class ChatRetrieveSerializer(serializers.ModelSerializer):
    """ Chat Retrieve Serializer """
    details = serializers.SerializerMethodField()

    def get_details(self, obj):
        request = self.context['request']

        if obj.chat_type == ChatType.DIALOG:
            return UserShortReadSerializer(
                obj.members.exclude(uuid=request.user.uuid).first(),
                context={'request': request},
            ).data

        if obj.chat_type == ChatType.GROUP:
            group_data = GroupChatRetrieveSerializer(
                obj.group_details,
                context={'request': request},
            ).data
            group_data['member_count'] = obj.members.all().count()
            return group_data

        return None

    class Meta:
        model = Chat
        fields = [
            'uuid',
            'chat_type',
            'details',
        ]
