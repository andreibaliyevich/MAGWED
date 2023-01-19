from rest_framework import serializers
from accounts.serializers import UserShortReadSerializer
from main.serializers import HashtagSerializer
from .models import Album, Photo


class AlbumShortReadSerializer(serializers.ModelSerializer):
    """ Album Short Read Serializer """
    
    class Meta:
        model = Album
        fields = [
            'id',
            'title',
            'thumbnail',
        ]


class AlbumListSerializer(serializers.ModelSerializer):
    """ Album List Serializer """
    owner = UserShortReadSerializer(read_only=True)

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
    owner = UserShortReadSerializer(read_only=True)
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

    class Meta:
        model = Photo
        fields = [
            'id',
            'thumbnail',
        ]


class PhotoListSerializer(serializers.ModelSerializer):
    """ Photo List Serializer """
    owner = UserShortReadSerializer(read_only=True)

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
    owner = UserShortReadSerializer(read_only=True)
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
