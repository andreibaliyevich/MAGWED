from contextlib import suppress
from exif import Image as ExifImage
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.permissions import UserIsOrganizer
from .models import Album, Photo
from .pagination import PortfolioPagination
from .serializers import (
    AlbumListCreateSerializer,
    AlbumImageSerializer,
    AlbumRUDSerializer,
    AlbumListSerializer,
    AlbumDetailSerializer,
    PhotoListCreateSerializer,
    PhotoRUDSerializer,
    PhotoListSerializer,
    PhotoDetailSerializer,
)


class AlbumListCreateView(generics.ListCreateAPIView):
    """ Album List Create View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    serializer_class = AlbumListCreateSerializer

    def get_queryset(self):
        queryset = Album.objects.filter(owner=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user,
            thumbnail=self.request.data['image'],
        )


class AlbumImageUpdateView(generics.UpdateAPIView):
    """ Album Image Update View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    lookup_field = 'uuid'
    serializer_class = AlbumImageSerializer

    def get_queryset(self):
        queryset = Album.objects.filter(owner=self.request.user)
        return queryset

    def perform_update(self, serializer):
        serializer.save(thumbnail=self.request.data['image'])


class AlbumRUDView(generics.RetrieveUpdateDestroyAPIView):
    """ Album Retrieve Update Destroy View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    lookup_field = 'uuid'
    serializer_class = AlbumRUDSerializer

    def get_queryset(self):
        queryset = Album.objects.filter(owner=self.request.user)
        return queryset


class AlbumListView(generics.ListAPIView):
    """ Album List View """
    permission_classes = [AllowAny]
    queryset = Album.objects.all()
    serializer_class = AlbumListSerializer
    pagination_class = PortfolioPagination


class AlbumDetailView(generics.RetrieveAPIView):
    """ Album Detail View """
    permission_classes = [AllowAny]
    lookup_field = 'uuid'
    serializer_class = AlbumDetailSerializer


class PhotoListCreateView(generics.ListCreateAPIView):
    """ Photo List Create View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    serializer_class = PhotoListCreateSerializer

    def get_queryset(self):
        queryset = Photo.objects.filter(
            owner=self.request.user,
            album__exact=None,
        )
        return queryset

    def perform_create(self, serializer):
        extra_data = {
            'owner': self.request.user,
            'thumbnail': self.request.data['image'],
        }

        exif_img = ExifImage(self.request.data['image'])
        with suppress(Exception):
            extra_data['device'] = f'{ exif_img.make } { exif_img.model }'
        with suppress(Exception):
            extra_data['f_number'] = exif_img.f_number
        with suppress(Exception):
            exposure_time = f'1/{ int(1 / float(exif_img.exposure_time)) }'
            extra_data['exposure_time'] = exposure_time
        with suppress(Exception):
            extra_data['focal_length'] = exif_img.focal_length
        with suppress(Exception):
            photographic_sensitivity = exif_img.photographic_sensitivity
            extra_data['photographic_sensitivity'] = photographic_sensitivity

        serializer.save(**extra_data)


class PhotoRUDView(generics.RetrieveUpdateDestroyAPIView):
    """ Photo Retrieve Update Destroy View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    lookup_field = 'uuid'
    serializer_class = PhotoRUDSerializer

    def get_queryset(self):
        queryset = Photo.objects.filter(owner=self.request.user)
        return queryset


class PhotoListView(generics.ListAPIView):
    """ Photo List View """
    permission_classes = [AllowAny]
    queryset = Photo.objects.all()
    serializer_class = PhotoListSerializer
    pagination_class = PortfolioPagination


class PhotoDetailView(generics.RetrieveAPIView):
    """ Photo Detail View """
    permission_classes = [AllowAny]
    lookup_field = 'uuid'
    serializer_class = PhotoDetailSerializer
