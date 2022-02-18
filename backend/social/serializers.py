from rest_framework import serializers
from accounts.serializers import MWUserSerializer
from accounts.models import MWUser
from accounts.serializers import MWUserSerializer
from portfolio.models import Album, Photo
from portfolio.serializers import AlbumListSerializer, PhotoListSerializer
from .models import Notification, Comment


class ContentObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the 'content_object' generic relationship.
    """

    def to_representation(self, value):
        if isinstance(value, MWUser):
            serializer = MWUserSerializer(value)
        elif isinstance(value, Album):
            serializer = AlbumListSerializer(value)
        elif isinstance(value, Photo):
            serializer = PhotoListSerializer(value)
        else:
            raise Exception('Unexpected type of tagged object')
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


CommentListSerializer._declared_fields['comments'] = CommentListSerializer(
    many=True)


class CommentCreateSerializer(serializers.ModelSerializer):
    """ Comment Create Serializer """

    class Meta:
        model = Comment
        fields = [
            'content',
        ]
