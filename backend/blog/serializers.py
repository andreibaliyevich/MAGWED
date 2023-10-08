from rest_framework import serializers
from accounts.serializers import UserShortReadSerializer
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


class ArticleDetailSerializer(serializers.ModelSerializer):
    """ Article Detail Serializer """
    author = UserShortReadSerializer(read_only=True)

    class Meta:
        model = Article
        fields = [
            'author',
            'categories',
            'translated_title',
            'image',
            'content',
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
