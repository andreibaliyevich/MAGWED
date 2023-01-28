from rest_framework import serializers
from accounts.serializers import UserShortReadSerializer
from blog.models import Article
from blog.serializers import ArticleShortReadSerializer
from portfolio.models import Album, Photo
from portfolio.serializers import (
    AlbumShortReadSerializer,
    PhotoShortReadSerializer,
)
from social.models import Follow, Comment, Review
from .models import Notification


class NotificationObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the 'content_object' generic relationship.
    """

    def to_representation(self, value):
        if isinstance(value, Follow):
            return None
        elif isinstance(value, Article):
            serializer = ArticleShortReadSerializer(value, context=self.context)
        elif isinstance(value, Album):
            serializer = AlbumShortReadSerializer(value, context=self.context)
        elif isinstance(value, Photo):
            serializer = PhotoShortReadSerializer(value, context=self.context)
        elif isinstance(value, Comment):
            return None
        elif isinstance(value, Review):
            return None
        else:
            raise Exception('Unexpected type of content object')
        return serializer.data


class NotificationListSerializer(serializers.ModelSerializer):
    """ Notification List Serializer """
    initiator = UserShortReadSerializer(read_only=True)
    content_object = NotificationObjectRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'initiator',
            'reason',
            'content_object',
            'viewed',
            'created_at',
        ]
