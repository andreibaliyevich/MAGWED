from rest_framework import serializers
from accounts.serializer_fields import UserSerializerField
from main.serializer_fields import HashtagSerializerField
from social.serializer_fields import CommentListSerializerField
from .models import Category, Article


class CategoryListSerializer(serializers.ModelSerializer):
    """ Category List Serializer """

    class Meta:
        model = Category
        fields = [
            'slug',
            'get_translated_name',
            'get_absolute_url',
        ]


class ArticleListSerializer(serializers.ModelSerializer):
    """ Article List Serializer """
    categories = CategoryListSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = [
            'slug',
            'categories',
            'get_translated_title',
            'thumbnail',
            'published_at',
            'num_views',
            'get_absolute_url',
        ]


class CategoryDetailSerializer(serializers.ModelSerializer):
    """ Category Detail Serializer """
    article_set = ArticleListSerializer(read_only=True, many=True)

    class Meta:
        model = Category
        fields = [
            'slug',
            'get_translated_name',
            'get_translated_meta_description',
            'get_translated_meta_keywords',
            'get_absolute_url',
            'article_set',
        ]


class ArticleDetailSerializer(serializers.ModelSerializer):
    """ Article Detail Serializer """
    author = UserSerializerField(read_only=True)
    categories = CategoryListSerializer(read_only=True, many=True)
    hashtags = HashtagSerializerField(read_only=True, many=True)
    comments = CommentListSerializerField(read_only=True, many=True)

    class Meta:
        model = Article
        fields = [
            'slug',
            'author',
            'categories',
            'get_translated_title',
            'get_translated_meta_description',
            'get_translated_meta_keywords',
            'image',
            'content',
            'hashtags',
            'published_at',
            'num_views',
            'comments',
            'get_absolute_url',
        ]
