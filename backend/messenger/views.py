from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Conversation
from .serializers import ConversationSerializer


class ConversationListView(generics.ListAPIView):
    """ Conversation List View """
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        queryset = Conversation.objects.filter(members=self.request.user)
        return queryset
