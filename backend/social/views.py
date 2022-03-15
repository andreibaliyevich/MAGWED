from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Notification, Comment
from .serializers import (
    NotificationListSerializer,
    CommentCreateSerializer,
)


class NotificationListView(generics.ListAPIView):
    """ Notification List View """
    queryset = Notification.objects.all()
    serializer_class = NotificationListSerializer


class CommentCreateView(generics.CreateAPIView):
    """ Comment Create View """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
