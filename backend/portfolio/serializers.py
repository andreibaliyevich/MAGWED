from rest_framework import serializers
from accounts.serializer_fields import OrganizerSerializerField
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
            'get_absolute_url',
        ]


class AlbumDetailSerializer(serializers.ModelSerializer):
    """ Album Detail Serializer """
    owner = OrganizerSerializerField(read_only=True)
    comments = CommentListSerializerField(read_only=True, many=True)

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
            'get_absolute_url',
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
            'get_absolute_url',
        ]


class PhotoDetailSerializer(serializers.ModelSerializer):
    """ Photo Detail Serializer """
    owner = OrganizerSerializerField(read_only=True)
    comments = CommentListSerializerField(read_only=True, many=True)

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
            'get_absolute_url',
        ]



