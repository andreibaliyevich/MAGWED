from rest_framework import generics
from .models import Organizer
from .serializers import OrganizerListSerializer, OrganizerDetailSerializer


class OrganizerListView(generics.ListAPIView):
    """ Organizer List View """
    queryset = Organizer.objects.all()
    serializer_class = OrganizerListSerializer


class OrganizerDetailView(generics.RetrieveAPIView):
    """ Organizer Detail View """
    queryset = Organizer.objects.all()
    lookup_field = 'profile_url'
    serializer_class = OrganizerDetailSerializer
