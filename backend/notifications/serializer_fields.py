from rest_framework import serializers
from blog.models import Article
from blog.serializers import ArticleListSerializer
from portfolio.models import Album, Photo
from portfolio.serializers import (
    AlbumShortReadSerializer,
    PhotoShortReadSerializer,
)
from social.models import Follow, Comment, Review


class NotificationObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the 'content_object' generic relationship.
    """

    def to_representation(self, value):
        if isinstance(value, Follow):
            serializer = { 'data': None }
        elif isinstance(value, Article):
            serializer = ArticleListSerializer(value)
        elif isinstance(value, Album):
            serializer = AlbumShortReadSerializer(value)
        elif isinstance(value, Photo):
            serializer = PhotoShortReadSerializer(value)
        elif isinstance(value, Comment):
            serializer = { 'data': None }
        elif isinstance(value, Review):
            serializer = { 'data': None }
        else:
            raise Exception('Unexpected type of content object')
        return serializer.data
