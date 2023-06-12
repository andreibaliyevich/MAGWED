from django_filters import rest_framework as filters
from .models import Album, Photo


class AlbumFilter(filters.FilterSet):
    """ Album Filter """

    class Meta:
        model = Album
        fields = [
            'owner',
            'editors_choice',
        ]

class PhotoFilter(filters.FilterSet):
    """ Photo Filter """
    album_is_null = filters.BooleanFilter(
        field_name='album',
        lookup_expr='isnull',
    )

    class Meta:
        model = Photo
        fields = [
            'owner',
            'album',
            'album_is_null',
            'editors_choice',
        ]
