from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import ugettext_lazy as _
from .choices import MessageType
from .models import Conversation
from .pagination import MessagePagination
from .serializers import (
    ConversationListSerializer,
    MessageFullReadSerializer,
    MessageCreateSerializer,
    ImageMessageSerializer,
    FileMessageSerializer,
)


class ConversationListView(generics.ListAPIView):
    """ Conversation List View """
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationListSerializer

    def get_queryset(self):
        queryset = Conversation.objects.filter(members=self.request.user)
        return queryset


class MessageListView(generics.ListAPIView):
    """ Message List View """
    permission_classes = [IsAuthenticated]
    serializer_class = MessageFullReadSerializer
    pagination_class = MessagePagination

    def validate_url(self, request, **kwargs):
        convo_id = kwargs.get('convo_id')
        try:
            self.conversation = Conversation.objects.get(id=convo_id)
        except Conversation.DoesNotExist:
            return False
        return request.user in self.conversation.members.all()

    def get_queryset(self):
        queryset = self.conversation.messages.all()
        return queryset

    def get(self, request, *args, **kwargs):
        if not self.validate_url(request, **kwargs):
            return Response(
                {'detail': _('Not found.')},
                status=status.HTTP_404_NOT_FOUND)
        return self.list(request, *args, **kwargs)


class ImageMessageView(APIView):
    """ Image Message View """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        msg_serializer = MessageCreateSerializer(
            data={'conversation': request.data['conversation']},
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
        return Response(msg_data, status=status.HTTP_200_OK)


class FileMessageView(APIView):
    """ File Message View """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        msg_serializer = MessageCreateSerializer(
            data={'conversation': request.data['conversation']},
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
        return Response(msg_data, status=status.HTTP_200_OK)
