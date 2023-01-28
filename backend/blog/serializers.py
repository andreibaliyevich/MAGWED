from rest_framework import serializers
from accounts.serializers import UserShortReadSerializer
from main.serializers import HashtagSerializer
from .models import Category, Article


class CategoryListSerializer(serializers.ModelSerializer):
    """ Category List Serializer """

    class Meta:
        model = Category
        fields = [
            'slug',
            'translated_name',
        ]


class ArticleListSerializer(serializers.ModelSerializer):
    """ Article List Serializer """
    categories = CategoryListSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = [
            'slug',
            'categories',
            'translated_title',
            'thumbnail',
            'published_at',
            'num_views',
        ]


class CategoryDetailSerializer(serializers.ModelSerializer):
    """ Category Detail Serializer """
    articles = ArticleListSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = [
            'slug',
            'translated_name',
            'translated_meta_description',
            'translated_meta_keywords',
            'articles',
        ]


class ArticleDetailSerializer(serializers.ModelSerializer):
    """ Article Detail Serializer """
    author = UserShortReadSerializer(read_only=True)
    categories = CategoryListSerializer(read_only=True, many=True)
    hashtags = HashtagSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = [
            'slug',
            'author',
            'categories',
            'translated_title',
            'translated_meta_description',
            'translated_meta_keywords',
            'image',
            'content',
            'hashtags',
            'published_at',
            'num_views',
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
