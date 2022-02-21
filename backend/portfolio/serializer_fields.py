from rest_framework import serializers
from accounts.serializer_fields import OrganizerSerializerField
from .models import Album, Photo


class AlbumSerializerField(serializers.ModelSerializer):
    """ Album Serializer Field """
    owner = OrganizerSerializerField(read_only=True)

    class Meta:
        model = Album
        fields = [
            'owner',
            'title',
            'thumbnail',
        ]


class PhotoSerializerField(serializers.ModelSerializer):
    """ Photo Serializer Field """
    owner = OrganizerSerializerField(read_only=True)

    class Meta:
        model = Photo
        fields = [
            'owner',
            'thumbnail',
        ]
