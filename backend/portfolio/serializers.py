from rest_framework import serializers
from accounts.serializer_fields import OrganizerSerializerField
from main.serializers import HashtagSerializer
from social.serializer_fields import CommentListSerializerField
from .models import Album, Photo


class AlbumListSerializer(serializers.ModelSerializer):
    """ Album List Serializer """
    owner = OrganizerSerializerField(read_only=True)

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
    owner = OrganizerSerializerField(read_only=True)
    comments = CommentListSerializerField(read_only=True, many=True)
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
            'comments',
        ]


class PhotoListSerializer(serializers.ModelSerializer):
    """ Photo List Serializer """
    owner = OrganizerSerializerField(read_only=True)

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
    owner = OrganizerSerializerField(read_only=True)
    comments = CommentListSerializerField(read_only=True, many=True)
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
            'comments',
        ]
