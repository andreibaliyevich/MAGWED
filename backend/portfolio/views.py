from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import UserIsOrganizer
from .models import Album, Photo
from .serializers import (
    AlbumListCreateSerializer,
    AlbumRUDSerializer,
    PhotoListCreateSerializer,
    PhotoRUDSerializer,
)


class AlbumListCreateView(generics.ListCreateAPIView):
    """ Album List Create View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    serializer_class = AlbumListCreateSerializer

    def get_queryset(self):
        queryset = Album.objects.filter(owner=self.request.user)
        return queryset


class AlbumRUDView(generics.RetrieveUpdateDestroyAPIView):
    """ Album Retrieve Update Destroy View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    lookup_field = 'uuid'
    serializer_class = AlbumRUDSerializer

    def get_queryset(self):
        queryset = Album.objects.filter(owner=self.request.user)
        return queryset


class PhotoListCreateView(generics.ListCreateAPIView):
    """ Photo List Create View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    serializer_class = PhotoListCreateSerializer

    def get_queryset(self):
        queryset = Photo.objects.filter(owner=self.request.user)
        return queryset


class PhotoRUDView(generics.RetrieveUpdateDestroyAPIView):
    """ Photo Retrieve Update Destroy View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    lookup_field = 'uuid'
    serializer_class = PhotoRUDSerializer

    def get_queryset(self):
        queryset = Photo.objects.filter(owner=self.request.user)
        return queryset
