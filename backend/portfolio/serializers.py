from rest_framework import serializers
from main.models import Hashtag
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
    image = serializers.ImageField(write_only=True)
    thumbnail = serializers.ImageField(read_only=True)
    description = serializers.CharField(write_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Album
        fields = [
            'uuid',
            'image',
            'thumbnail',
            'title',
            'description',
            'created_at',
        ]


class AlbumRUDSerializer(serializers.ModelSerializer):
    """ Album Retrieve Update Destroy Serializer """
    hashtags = serializers.PrimaryKeyRelatedField(
        queryset=Hashtag.objects.all(), many=True)

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
    image = serializers.ImageField(write_only=True)
    thumbnail = serializers.ImageField(read_only=True)
    title = serializers.CharField(read_only=True)
    uploaded_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Photo
        fields = [
            'uuid',
            'image',
            'thumbnail',
            'title',
            'uploaded_at',
        ]


class PhotoRUDSerializer(serializers.ModelSerializer):
    """ Photo Retrieve Update Destroy Serializer """
    image = serializers.ImageField(read_only=True)
    hashtags = serializers.PrimaryKeyRelatedField(
        queryset=Hashtag.objects.all(), many=True)
    uploaded_at = serializers.DateTimeField(read_only=True)
    num_views = serializers.IntegerField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    rating = serializers.IntegerField(read_only=True)

    def get_likes_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = Photo
        fields = [
            'uuid',
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
            'likes_count',
            'rating',
        ]
