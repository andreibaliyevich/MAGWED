from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import UserIsOrganizer
from .models import SocialLink
from .serializers import SocialLinkSerializer


class OrganizerLinkListCreateView(generics.ListCreateAPIView):
    """ Organizer Link List or Create View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    serializer_class = SocialLinkSerializer

    def get_queryset(self):
        queryset = SocialLink.objects.filter(user=self.request.user)
        return queryset


class OrganizerLinkRUDView(generics.RetrieveUpdateDestroyAPIView):
    """ Organizer Link Retrieve Update Destroy View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    serializer_class = SocialLinkSerializer

    def get_queryset(self):
        queryset = SocialLink.objects.filter(user=self.request.user)
        return queryset
