from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import ugettext_lazy as _
from .choices import MessageType
from .filters import MessageFilter
from .models import Chat, Message
from .pagination import MessagePagination
from .serializers import (
    ChatListSerializer,
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
            'content': request.data['content']
        })
        text_serializer.is_valid(raise_exception=True)
        text_serializer.save(message=msg)

        msg_data = MessageFullReadSerializer(
            msg,
            context={'request': request},
        ).data

        async_to_sync(channel_layer.group_send)(
            f'convo-{msg.chat.uuid}',
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

        images = request.FILES.getlist('content', None)
        for img in images:
            img_serializer = ImageMessageSerializer(data={'content': img})
            img_serializer.is_valid(raise_exception=True)
            img_serializer.save(message=msg)

        msg_data = MessageFullReadSerializer(
            msg,
            context={'request': request},
        ).data

        async_to_sync(channel_layer.group_send)(
            f'convo-{msg.chat.uuid}',
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

        files = request.FILES.getlist('content', None)
        for file in files:
            file_serializer = FileMessageSerializer(data={'content': file})
            file_serializer.is_valid(raise_exception=True)
            file_serializer.save(message=msg)

        msg_data = MessageFullReadSerializer(
            msg,
            context={'request': request},
        ).data

        async_to_sync(channel_layer.group_send)(
            f'convo-{msg.chat.uuid}',
            {
                'type': 'send_json_data',
                'action': 'new_msg',
                'data': msg_data,
            }
        )
        return Response(status=status.HTTP_201_CREATED)
