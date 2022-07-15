from rest_framework import serializers
from accounts.serializers import OrganizerShortReadSerializer
from main.serializers import HashtagSerializer
from .models import Album, Photo


class AlbumShortReadSerializer(serializers.ModelSerializer):
    """ Album Short Read Serializer """
    owner = OrganizerShortReadSerializer(read_only=True)

    class Meta:
        model = Album
        fields = [
            'owner',
            'title',
            'thumbnail',
        ]


class AlbumListSerializer(serializers.ModelSerializer):
    """ Album List Serializer """
    owner = OrganizerShortReadSerializer(read_only=True)

    class Meta:
        model = Album
        fields = [
            'id',
            'owner',
            'title',
            'thumbnail',
            'created_at',
            'num_views',
            'likes',
            'rating',
        ]


class AlbumDetailSerializer(serializers.ModelSerializer):
    """ Album Detail Serializer """
    owner = OrganizerShortReadSerializer(read_only=True)
    hashtags = HashtagSerializer(read_only=True, many=True)

    class Meta:
        model = Album
        fields = [
            'id',
            'owner',
            'title',
            'image',
            'description',
            'hashtags',
            'created_at',
            'num_views',
            'likes',
            'rating',
        ]


class PhotoShortReadSerializer(serializers.ModelSerializer):
    """ Photo Short Read Serializer """
    owner = OrganizerShortReadSerializer(read_only=True)

    class Meta:
        model = Photo
        fields = [
            'owner',
            'thumbnail',
        ]


class PhotoListSerializer(serializers.ModelSerializer):
    """ Photo List Serializer """
    owner = OrganizerShortReadSerializer(read_only=True)

    class Meta:
        model = Photo
        fields = [
            'id',
            'owner',
            'thumbnail',
            'uploaded_at',
            'num_views',
            'likes',
            'rating',
        ]


class PhotoDetailSerializer(serializers.ModelSerializer):
    """ Photo Detail Serializer """
    owner = OrganizerShortReadSerializer(read_only=True)
    hashtags = HashtagSerializer(read_only=True, many=True)

    class Meta:
        model = Photo
        fields = [
            'id',
            'owner',
            'album',
            'image',
            'device',
            'f_number',
            'exposure_time',
            'focal_length',
            'photographic_sensitivity',
            'description',
            'hashtags',
            'uploaded_at',
            'num_views',
            'likes',
            'rating',
        ]
