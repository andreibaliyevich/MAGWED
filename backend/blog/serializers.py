from rest_framework import serializers
from accounts.serializers import UserAuthorReadSerializer
from main.serializers import TagRelatedField
from .models import Category, Article


class ArticleListSerializer(serializers.ModelSerializer):
    """ Article List Serializer """

    class Meta:
        model = Article
        fields = [
            'slug',
            'categories',
            'translated_title',
            'thumbnail',
            'translated_description',
            'published_at',
        ]


class ArticleRetrieveSerializer(serializers.ModelSerializer):
    """ Article Retrieve Serializer """
    author = UserAuthorReadSerializer(read_only=True)
    tags = TagRelatedField(read_only=True, many=True)

    class Meta:
        model = Article
        fields = [
            'uuid',
            'author',
            'categories',
            'translated_title',
            'image',
            'translated_content',
            'tags',
            'published_at',
            'view_count',
        ]


class ArticleShortReadSerializer(serializers.ModelSerializer):
    """ Article Short Read Serializer """

    class Meta:
        model = Article
        fields = [
            'slug',
            'translated_title',
            'thumbnail',
        ]
