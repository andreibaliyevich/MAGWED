from django_filters import rest_framework as filters
from .models import Album, Photo


class AlbumFilter(filters.FilterSet):
    """ Album Filter """

    class Meta:
        model = Album
        fields = [
            'owner',
        ]

class PhotoFilter(filters.FilterSet):
    """ Photo Filter """

    class Meta:
        model = Photo
        fields = [
            'owner',
            'album',
        ]