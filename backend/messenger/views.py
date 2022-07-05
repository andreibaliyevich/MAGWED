from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Chat
from .serializers import ChatSerializer


class ChatListView(generics.ListAPIView):
    """ Chat List View """
    permission_classes = [IsAuthenticated]
    serializer_class = ChatSerializer

    def get_queryset(self):
        queryset = Chat.objects.filter(members=self.request.user)
        return queryset
