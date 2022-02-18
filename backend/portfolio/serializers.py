from rest_framework import serializers
from accounts.serializers import OrganizerSerializer
from .models import Album, Photo


class AlbumListSerializer(serializers.ModelSerializer):
    """ Album List Serializer """
    owner = OrganizerSerializer()

    class Meta:
        model = Album
        fields = [
            'owner',
            'title',
            'thumbnail',
        ]


class PhotoListSerializer(serializers.ModelSerializer):
    """ Photo List Serializer """
    owner = OrganizerSerializer()

    class Meta:
        model = Photo
        fields = [
            'owner',
            'thumbnail',
        ]
