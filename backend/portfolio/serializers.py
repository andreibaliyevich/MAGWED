from rest_framework import serializers
from main.serializers import TagRelatedField
from accounts.serializers import UserBriefReadSerializer
from .models import Album, Photo


class AlbumShortReadSerializer(serializers.ModelSerializer):
    """ Album Short Read Serializer """
    
    class Meta:
        model = Album
        fields = [
            'uuid',
            'thumbnail',
            'title',
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
    album = serializers.PrimaryKeyRelatedField(
        write_only=True,
        required=False,
        queryset=Album.objects.all(),
    )
    image = serializers.ImageField(write_only=True)
    thumbnail = serializers.ImageField(read_only=True)
    title = serializers.CharField(read_only=True)
    uploaded_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Photo
        fields = [
            'uuid',
            'album',
            'image',
            'thumbnail',
            'title',
            'uploaded_at',
        ]


class PhotoRUDSerializer(serializers.ModelSerializer):
    """ Photo Retrieve Update Destroy Serializer """
    image = serializers.ImageField(read_only=True)
    tags = TagRelatedField(many=True)
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
            'tags',
            'uploaded_at',
            'num_views',
            'likes_count',
            'rating',
        ]


class OwnerPhotoListSerializer(serializers.ModelSerializer):
    """ Owner Photo List Serializer """
    likes_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = Photo
        fields = [
            'uuid',
            'thumbnail',
            'title',
            'num_views',
            'likes_count',
            'rating',
        ]


class PhotoListSerializer(serializers.ModelSerializer):
    """ Photo List Serializer """
    owner = UserBriefReadSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = Photo
        fields = [
            'uuid',
            'owner',
            'thumbnail',
            'title',
            'num_views',
            'likes_count',
            'rating',
        ]


class PhotoDetailSerializer(serializers.ModelSerializer):
    """ Photo Detail Serializer """
    album = AlbumShortReadSerializer(read_only=True, many=True)
    tags = TagRelatedField(read_only=True, many=True)
    likes_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = Photo
        fields = [
            'uuid',
            'album',
            'image',
            'device',
            'f_number',
            'exposure_time',
            'focal_length',
            'photographic_sensitivity',
            'title',
            'description',
            'tags',
            'uploaded_at',
            'num_views',
            'likes_count',
            'rating',
        ]


class AlbumListCreateSerializer(serializers.ModelSerializer):
    """ Album List Create Serializer """
    image = serializers.ImageField(write_only=True)
    thumbnail = serializers.ImageField(read_only=True)
    description = serializers.CharField(write_only=True, allow_blank=True)
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


class AlbumImageSerializer(serializers.ModelSerializer):
    """ Album Image Serializer """

    class Meta:
        model = Album
        fields = ['image']


class AlbumRUDSerializer(serializers.ModelSerializer):
    """ Album Retrieve Update Destroy Serializer """
    image = serializers.ImageField(read_only=True)
    tags = TagRelatedField(many=True)
    created_at = serializers.DateTimeField(read_only=True)
    num_views = serializers.IntegerField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    rating = serializers.IntegerField(read_only=True)
    photos = PhotoListCreateSerializer(read_only=True, many=True)

    def get_likes_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = Album
        fields = [
            'uuid',
            'image',
            'title',
            'description',
            'tags',
            'created_at',
            'num_views',
            'likes_count',
            'rating',
            'photos',
        ]


class OwnerAlbumListSerializer(serializers.ModelSerializer):
    """ Owner Album List Serializer """
    likes_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = Album
        fields = [
            'uuid',
            'thumbnail',
            'title',
            'num_views',
            'likes_count',
            'rating',
        ]


class AlbumListSerializer(serializers.ModelSerializer):
    """ Album List Serializer """
    owner = UserBriefReadSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()

    def get_likes_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = Album
        fields = [
            'uuid',
            'owner',
            'thumbnail',
            'title',
            'num_views',
            'likes_count',
            'rating',
        ]


class AlbumDetailSerializer(serializers.ModelSerializer):
    """ Album Detail Serializer """
    tags = TagRelatedField(read_only=True, many=True)
    likes_count = serializers.SerializerMethodField()
    photos = PhotoListSerializer(read_only=True, many=True)

    def get_likes_count(self, obj):
        return obj.likes.count()

    class Meta:
        model = Album
        fields = [
            'uuid',
            'image',
            'title',
            'description',
            'tags',
            'created_at',
            'num_views',
            'likes_count',
            'rating',
            'photos',
        ]
