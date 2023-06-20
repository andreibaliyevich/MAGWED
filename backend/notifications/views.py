from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .pagination import NotificationPagination
from .serializers import NotificationListSerializer


class NotificationListView(generics.ListAPIView):
    """ Notification List View """
    permission_classes = [IsAuthenticated]
    serializer_class = NotificationListSerializer
    pagination_class = NotificationPagination

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
