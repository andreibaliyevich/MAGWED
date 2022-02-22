from rest_framework import generics
from .models import Album, Photo
from .serializers import (
    AlbumListSerializer,
    AlbumDetailSerializer,
    PhotoListSerializer,
    PhotoDetailSerializer,
)


class AlbumListView(generics.ListAPIView):
    """ Album List View """
    queryset = Album.objects.all()
    serializer_class = AlbumListSerializer


class AlbumDetailView(generics.RetrieveAPIView):
    """ Album Detail View """
    queryset = Album.objects.all()
    serializer_class = AlbumDetailSerializer


class PhotoListView(generics.ListAPIView):
    """ Photo List View """
    queryset = Photo.objects.all()
    serializer_class = PhotoListSerializer


class PhotoDetailView(generics.RetrieveAPIView):
    """ Photo Detail View """
    queryset = Photo.objects.all()
    serializer_class = PhotoDetailSerializer
