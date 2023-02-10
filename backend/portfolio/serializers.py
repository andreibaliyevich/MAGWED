from rest_framework import serializers
from main.serializers import HashtagSerializer
from .models import Album, Photo


class AlbumShortReadSerializer(serializers.ModelSerializer):
    """ Album Short Read Serializer """
    
    class Meta:
        model = Album
        fields = [
            'uuid',
            'title',
            'thumbnail',
        ]


class AlbumListCreateSerializer(serializers.ModelSerializer):
    """ Album List Create Serializer """

    class Meta:
        model = Album
        fields = [
            'uuid',
            'thumbnail',
            'title',
            'created_at',
        ]


class AlbumRUDSerializer(serializers.ModelSerializer):
    """ Album Retrieve Update Destroy Serializer """
    hashtags = HashtagSerializer(read_only=True, many=True)

    class Meta:
        model = Album
        fields = [
            'uuid',
            'owner',
            'image',
            'title',
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
            'uuid',
            'thumbnail',
            'title',
        ]


class PhotoListCreateSerializer(serializers.ModelSerializer):
    """ Photo List Create Serializer """

    class Meta:
        model = Photo
        fields = [
            'uuid',
            'thumbnail',
            'title',
            'uploaded_at',
        ]


class PhotoRUDSerializer(serializers.ModelSerializer):
    """ Photo Retrieve Update Destroy Serializer """
    hashtags = HashtagSerializer(read_only=True, many=True)

    class Meta:
        model = Photo
        fields = [
            'uuid',
            'owner',
            'album',
            'image',
            'device',
            'f_number',
            'exposure_time',
            'focal_length',
            'photographic_sensitivity',
            'title',
            'description',
            'hashtags',
            'uploaded_at',
            'num_views',
            'likes',
            'rating',
        ]
