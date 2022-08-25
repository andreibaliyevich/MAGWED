from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .choices import MessageType
from .models import Conversation
from .serializers import (
    ConversationSerializer,
    MessageCreateSerializer,
    ImageMessageSerializer,
    FileMessageSerializer,
    MessageFullReadSerializer,
)


class ConversationListView(generics.ListAPIView):
    """ Conversation List View """
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        queryset = Conversation.objects.filter(members=self.request.user)
        return queryset


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

        msg_data = MessageFullReadSerializer(msg).data
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

        msg_data = MessageFullReadSerializer(msg).data
        return Response(msg_data, status=status.HTTP_200_OK)
