from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from .filters import OrganizerFilter
from .models import Organizer
from .serializers import OrganizerListSerializer, OrganizerDetailSerializer


class OrganizerListView(generics.ListAPIView):
    """ Organizer List View """
    queryset = Organizer.objects.all()
    serializer_class = OrganizerListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrganizerFilter


class OrganizerDetailView(generics.RetrieveAPIView):
    """ Organizer Detail View """
    queryset = Organizer.objects.all()
    lookup_field = 'profile_url'
    serializer_class = OrganizerDetailSerializer
