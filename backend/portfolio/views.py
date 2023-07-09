from contextlib import suppress
from exif import Image as ExifImage
from rest_framework import filters, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from accounts.permissions import UserIsOrganizer
from .filters import AlbumFilter, PhotoFilter
from .models import Album, Photo
from .pagination import PortfolioPagination
from .serializers import (
    AlbumListCreateSerializer,
    AlbumImageSerializer,
    AlbumRUDSerializer,
    AlbumListShortSerializer,
    AlbumListSerializer,
    AlbumDetailSerializer,
    AlbumUUIDSerializer,
    PhotoListCreateSerializer,
    PhotoRUDSerializer,
    PhotoListShortSerializer,
    PhotoListSerializer,
    PhotoDetailSerializer,
    PhotoUUIDSerializer,
)


class AlbumListCreateView(generics.ListCreateAPIView):
    """ Album List Create View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    serializer_class = AlbumListCreateSerializer

    def get_queryset(self):
        return Album.objects.filter(owner=self.request.user)

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
        return Album.objects.filter(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(thumbnail=self.request.data['image'])


class AlbumRUDView(generics.RetrieveUpdateDestroyAPIView):
    """ Album Retrieve Update Destroy View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    lookup_field = 'uuid'
    serializer_class = AlbumRUDSerializer

    def get_queryset(self):
        return Album.objects.filter(owner=self.request.user)


class AlbumListView(generics.ListAPIView):
    """ Album List View """
    permission_classes = [AllowAny]
    queryset = Album.objects.all()
    pagination_class = PortfolioPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = AlbumFilter
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.GET.get('owner', None):
            return AlbumListShortSerializer
        return AlbumListSerializer


class AlbumDetailView(generics.RetrieveAPIView):
    """ Album Detail View """
    permission_classes = [AllowAny]
    queryset = Album.objects.all()
    lookup_field = 'uuid'
    serializer_class = AlbumDetailSerializer


class AlbumUpViewCountView(APIView):
    """ Album Up View Count View """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = AlbumUUIDSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        album = serializer.album

        album.view_count += 1
        album.save(update_fields=['view_count'])

        return Response(status=status.HTTP_204_NO_CONTENT)


class AlbumLikeView(APIView):
    """ Album Like View """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = AlbumUUIDSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        album = serializer.album

        try:
            album.likes.add(request.user)
        except:
            return Response(
                {'detail': _('You already liked this album!')},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        serializer = AlbumUUIDSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        album = serializer.album

        try:
            album.likes.remove(request.user)
        except:
            return Response(
                {'detail': _('You do not like this album!')},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class PhotoListCreateView(generics.ListCreateAPIView):
    """ Photo List Create View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    serializer_class = PhotoListCreateSerializer

    def get_queryset(self):
        return Photo.objects.filter(
            owner=self.request.user,
            album__exact=None,
        )

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
        return Photo.objects.filter(owner=self.request.user)


class PhotoListView(generics.ListAPIView):
    """ Photo List View """
    permission_classes = [AllowAny]
    queryset = Photo.objects.all()
    pagination_class = PortfolioPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PhotoFilter
    ordering_fields = ['uploaded_at', 'rating']
    ordering = ['-uploaded_at']

    def get_serializer_class(self):
        if (self.request.GET.get('owner', None)
                or self.request.GET.get('album', None)):
            return PhotoListShortSerializer
        return PhotoListSerializer


class PhotoDetailView(generics.RetrieveAPIView):
    """ Photo Detail View """
    permission_classes = [AllowAny]
    queryset = Photo.objects.all()
    lookup_field = 'uuid'
    serializer_class = PhotoDetailSerializer


class PhotoUpViewCountView(APIView):
    """ Photo Up View Count View """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PhotoUUIDSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        photo = serializer.photo

        photo.view_count += 1
        photo.save(update_fields=['view_count'])

        return Response(status=status.HTTP_204_NO_CONTENT)


class PhotoLikeView(APIView):
    """ Photo Like View """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PhotoUUIDSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        photo = serializer.photo

        try:
            photo.likes.add(request.user)
        except:
            return Response(
                {'detail': _('You already liked this photo!')},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        serializer = PhotoUUIDSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        photo = serializer.photo

        try:
            photo.likes.remove(request.user)
        except:
            return Response(
                {'detail': _('You do not like this photo!')},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)
