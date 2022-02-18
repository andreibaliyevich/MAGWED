from rest_framework import serializers
from social.serializers import CommentListSerializer
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
    categories = CategoryListSerializer(many=True)

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
    article_set = ArticleListSerializer(many=True)

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
    author = serializers.SlugRelatedField(slug_field='name', read_only=True)
    categories = CategoryListSerializer(many=True)
    hashtags = serializers.SlugRelatedField(
        slug_field='name',
        many=True,
        read_only=True,
    )
    comments = CommentListSerializer(many=True)

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
