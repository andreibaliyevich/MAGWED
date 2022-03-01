from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from .filters import OrganizerFilter
from .models import Organizer
from .serializers import (
    RegistrationSerializer,
    OrganizerListSerializer,
    OrganizerDetailSerializer,
)


UserModel = get_user_model()


class RegistrationView(generics.CreateAPIView):
    """ Registration View """
    queryset = UserModel.objects.all()
    serializer_class = RegistrationSerializer


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
