from rest_framework import serializers
from accounts.models import MWUser
from accounts.serializers import UserShortReadSerializer
from portfolio.models import Album, Photo
from portfolio.serializers import (
    AlbumShortReadSerializer,
    PhotoShortReadSerializer,
)


class ContentObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the 'content_object' generic relationship.
    """

    def to_representation(self, value):
        if isinstance(value, MWUser):
            serializer = UserShortReadSerializer(value)
        elif isinstance(value, Album):
            serializer = AlbumShortReadSerializer(value)
        elif isinstance(value, Photo):
            serializer = PhotoShortReadSerializer(value)
        else:
            raise Exception('Unexpected type of content object')
        return serializer.data
