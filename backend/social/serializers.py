from rest_framework import serializers
from accounts.models import MWUser
from accounts.serializers import MWUserSerializer, OrganizerSerializer
from portfolio.models import Album, Photo
# from portfolio.serializers import AlbumShortSerializer, PhotoShortSerializer
from .models import Notification, Comment


class AlbumShortSerializer(serializers.ModelSerializer):
    """ Album Short Serializer """
    owner = OrganizerSerializer()

    class Meta:
        model = Album
        fields = [
            'owner',
            'title',
            'thumbnail',
        ]


class PhotoShortSerializer(serializers.ModelSerializer):
    """ Photo Short Serializer """
    owner = OrganizerSerializer()

    class Meta:
        model = Photo
        fields = [
            'owner',
            'thumbnail',
        ]


class ContentObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the 'content_object' generic relationship.
    """

    def to_representation(self, value):
        if isinstance(value, MWUser):
            serializer = MWUserSerializer(value)
        elif isinstance(value, Album):
            serializer = AlbumShortSerializer(value)
        elif isinstance(value, Photo):
            serializer = PhotoShortSerializer(value)
        else:
            raise Exception('Unexpected type of content object')
        return serializer.data


class NotificationListSerializer(serializers.ModelSerializer):
    """ Notification List Serializer """
    content_object = ContentObjectRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'content_object',
            'viewed',
            'created_at',
        ]


class CommentListSerializer(serializers.ModelSerializer):
    """ Comment List Serializer """
    user = MWUserSerializer()

    class Meta:
        model = Comment
        fields = [
            'user',
            'content',
            'created_at',
            'comments',
        ]

    def get_fields(self):
        fields = super(CommentListSerializer, self).get_fields()
        fields['comments'] = CommentListSerializer(many=True)
        return fields


class CommentCreateSerializer(serializers.ModelSerializer):
    """ Comment Create Serializer """

    class Meta:
        model = Comment
        fields = [
            'content',
        ]
