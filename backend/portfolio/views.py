from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Album, Photo
from .serializers import (
    AlbumListSerializer,
    AlbumDetailSerializer,
    PhotoListSerializer,
    PhotoDetailSerializer,
)


class AlbumListView(APIView):
    """ Album List View """

    def get(self, request):
        albums = Album.objects.all()
        serializer = AlbumListSerializer(albums, many=True)
        return Response(serializer.data)


class AlbumDetailView(APIView):
    """ Album Detail View """

    def get(self, request, album_id):
        album = Album.objects.get(id=album_id)
        serializer = AlbumDetailSerializer(album)
        return Response(serializer.data)


class PhotoListView(APIView):
    """ Photo List View """

    def get(self, request):
        photos = Photo.objects.all()
        serializer = PhotoListSerializer(photos, many=True)
        return Response(serializer.data)


class PhotoDetailView(APIView):
    """ Photo Detail View """

    def get(self, request, photo_id):
        photo = Photo.objects.get(id=photo_id)
        serializer = PhotoDetailSerializer(photo)
        return Response(serializer.data)
