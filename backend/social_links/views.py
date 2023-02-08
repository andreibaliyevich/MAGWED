from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import UserIsOrganizer
from .models import SocialLink
from .serializers import SocialLinkSerializer


class SocialLinkListCreateView(generics.ListCreateAPIView):
    """ Social Link List Create View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    serializer_class = SocialLinkSerializer

    def get_queryset(self):
        queryset = SocialLink.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SocialLinkRUDView(generics.RetrieveUpdateDestroyAPIView):
    """ Social Link Retrieve Update Destroy View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    serializer_class = SocialLinkSerializer

    def get_queryset(self):
        queryset = SocialLink.objects.filter(user=self.request.user)
        return queryset
