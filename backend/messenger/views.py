from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import ugettext_lazy as _
from accounts.serializers import UserUUIDSerializer
from .choices import ChatType, MessageType
from .filters import MessageFilter
from .models import Chat, Message
from .pagination import MessagePagination
from .serializers import (
    ChatListSerializer,
    ChatCreateSerializer,
    GroupChatListCreateSerializer,
    ChatRetrieveSerializer,
    MessageFullReadSerializer,
    MessageCreateSerializer,
    TextMessageSerializer,
    ImageMessageSerializer,
    FileMessageSerializer,
)


channel_layer = get_channel_layer()


class ChatListView(generics.ListAPIView):
    """ Chat List View """
    permission_classes = [IsAuthenticated]
    serializer_class = ChatListSerializer

    def get_queryset(self):
        return Chat.objects.filter(members=self.request.user)


class ChatCreateView(APIView):
    """ Chat Create View """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        chat_serializer = ChatCreateSerializer(
            data={
                'chat_type': request.data['chat_type'],
                'members': request.data.getlist('members', []),
            },
            context={'request': request},
        )
        chat_serializer.is_valid(raise_exception=True)
        chat_valid_data = chat_serializer.validated_data
        chat = None

        if chat_valid_data['chat_type'] == ChatType.DIALOG:
            dialog_chats = Chat.objects.filter(
                chat_type=ChatType.DIALOG,
                members=request.user,
            )
            for dialog in dialog_chats:
                if chat_valid_data['members'][0] == dialog.members.exclude(
                        uuid=request.user.uuid).first():
                    chat = dialog
                    break
            if chat is None:
                chat = chat_serializer.save()
                chat.members.add(request.user)
            else:
                return Response(chat.uuid, status=status.HTTP_400_BAD_REQUEST)
        elif chat_valid_data['chat_type'] == ChatType.GROUP:
            chat = chat_serializer.save()
            chat.members.add(request.user)

            group_chat_serializer = GroupChatListCreateSerializer(
                data={
                    'name': request.data['name'],
                    'image': request.data['image'],
                },
                context={'request': request},
            )
            group_chat_serializer.is_valid(raise_exception=True)
            group_chat_serializer.save(chat=chat, owner=request.user)

        chat_data = ChatListSerializer(
            chat,
            context={'request': request},
        ).data
        return Response(chat_data, status=status.HTTP_201_CREATED)


class ChatRetrieveView(generics.RetrieveAPIView):
    """ Chat Retrieve View """
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'
    serializer_class = ChatRetrieveSerializer

    def get_queryset(self):
        return Chat.objects.filter(members=self.request.user)


class MessageListView(generics.ListAPIView):
    """ Message List View """
    permission_classes = [IsAuthenticated]
    serializer_class = MessageFullReadSerializer
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        return Message.objects.filter(chat__members=self.request.user)


class TextMessageView(APIView):
    """ Text Message View """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        msg_serializer = MessageCreateSerializer(
            data={'chat': request.data['chat']},
            context={'request': request},
        )
        msg_serializer.is_valid(raise_exception=True)
        msg = msg_serializer.save(
            sender=request.user,
            msg_type=MessageType.TEXT,
        )

        text_serializer = TextMessageSerializer(data={
            'content': request.data['content']})
        text_serializer.is_valid(raise_exception=True)
        text_serializer.save(message=msg)

        msg_data = MessageFullReadSerializer(
            msg,
            context={'request': request},
        ).data

        async_to_sync(channel_layer.group_send)(
            f'chat-{msg.chat.uuid}',
            {
                'type': 'send_json_data',
                'action': 'new_msg',
                'data': msg_data,
            }
        )
        return Response(status=status.HTTP_201_CREATED)


class ImageMessageView(APIView):
    """ Image Message View """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        msg_serializer = MessageCreateSerializer(
            data={'chat': request.data['chat']},
            context={'request': request},
        )
        msg_serializer.is_valid(raise_exception=True)
        msg = msg_serializer.save(
            sender=request.user,
            msg_type=MessageType.IMAGES,
        )

        images = request.data.getlist('content', None)
        for img in images:
            img_serializer = ImageMessageSerializer(data={'content': img})
            img_serializer.is_valid(raise_exception=True)
            img_serializer.save(message=msg)

        msg_data = MessageFullReadSerializer(
            msg,
            context={'request': request},
        ).data

        async_to_sync(channel_layer.group_send)(
            f'chat-{msg.chat.uuid}',
            {
                'type': 'send_json_data',
                'action': 'new_msg',
                'data': msg_data,
            }
        )
        return Response(status=status.HTTP_201_CREATED)


class FileMessageView(APIView):
    """ File Message View """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        msg_serializer = MessageCreateSerializer(
            data={'chat': request.data['chat']},
            context={'request': request},
        )
        msg_serializer.is_valid(raise_exception=True)
        msg = msg_serializer.save(
            sender=request.user,
            msg_type=MessageType.FILES,
        )

        files = request.data.getlist('content', None)
        for file in files:
            file_serializer = FileMessageSerializer(data={'content': file})
            file_serializer.is_valid(raise_exception=True)
            file_serializer.save(message=msg)

        msg_data = MessageFullReadSerializer(
            msg,
            context={'request': request},
        ).data

        async_to_sync(channel_layer.group_send)(
            f'chat-{msg.chat.uuid}',
            {
                'type': 'send_json_data',
                'action': 'new_msg',
                'data': msg_data,
            }
        )
        return Response(status=status.HTTP_201_CREATED)


class WriteMessageView(APIView):
    """ Write Message View """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_serializer = UserUUIDSerializer(data={
            'uuid': request.data['uuid']})
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.user

        chat = None
        dialog_chats = Chat.objects.filter(
            chat_type=ChatType.DIALOG,
            members=request.user,
        )
        for dialog in dialog_chats:
            if user == dialog.members.exclude(uuid=request.user.uuid).first():
                chat = dialog
                break
        if chat is None:
            chat = Chat.objects.create(chat_type=ChatType.DIALOG)
            chat.members.add(request.user, user)

        msg = Message.objects.create(
            chat=chat,
            sender=request.user,
            msg_type=MessageType.TEXT,
        )

        text_serializer = TextMessageSerializer(data={
            'content': request.data['content']})
        text_serializer.is_valid(raise_exception=True)
        text_serializer.save(message=msg)

        msg_data = MessageFullReadSerializer(
            msg,
            context={'request': request},
        ).data

        async_to_sync(channel_layer.group_send)(
            f'chat-{chat.uuid}',
            {
                'type': 'send_json_data',
                'action': 'new_msg',
                'data': msg_data,
            }
        )
        return Response(status=status.HTTP_201_CREATED)
