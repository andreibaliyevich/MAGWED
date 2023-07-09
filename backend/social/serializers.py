from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _
from accounts.serializers import UserShortReadSerializer
from blog.models import Article
from blog.serializers import ArticleShortReadSerializer
from portfolio.models import Album, Photo
from portfolio.serializers import (
    AlbumShortReadSerializer,
    PhotoShortReadSerializer,
)
from .models import SocialLink, Follow, Favorite, Comment, Review


UserModel = get_user_model()


class SocialLinkSerializer(serializers.ModelSerializer):
    """ Social Link Serializer """

    class Meta:
        model = SocialLink
        fields = [
            'uuid',
            'link_type',
            'link_url',
        ]


class SocialLinkReadSerializer(serializers.ModelSerializer):
    """ Social Link Read Serializer """

    class Meta:
        model = SocialLink
        fields = [
            'link_type',
            'link_url',
        ]


class FollowersSerializer(serializers.ModelSerializer):
    """ Followers Serializer """
    follower = UserShortReadSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = [
            'follower',
            'created_at',
        ]


class FollowingSerializer(serializers.ModelSerializer):
    """ Following Serializer """
    user = UserShortReadSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = [
            'user',
            'created_at',
        ]


class FavoriteContentObjectSerializer(serializers.Serializer):
    """ Favorite Content Object Serializer """
    content_type = serializers.CharField()
    object_uuid = serializers.UUIDField()

    def validate(self, data):
        if data['content_type'] == 'article':
            object_class = Article
        elif data['content_type'] == 'album':
            object_class = Album
        elif data['content_type'] == 'photo':
            object_class = Photo
        else:
            raise serializers.ValidationError({
                'content_type': _('Wrong content type.')})

        try:
            self.content_object = object_class.objects.get(
                uuid=data['object_uuid'])
        except object_class.DoesNotExist:
            raise serializers.ValidationError({
                'object_uuid': _('Wrong object uuid.')})

        return data


class FavoriteObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the 'content_object' generic relationship.
    """

    def to_representation(self, value):
        if isinstance(value, Article):
            serializer = ArticleShortReadSerializer(value, context=self.context)
        elif isinstance(value, Album):
            serializer = AlbumShortReadSerializer(value, context=self.context)
        elif isinstance(value, Photo):
            serializer = PhotoShortReadSerializer(value, context=self.context)
        else:
            raise Exception('Unexpected type of content object')
        return serializer.data


class FavoriteListSerializer(serializers.ModelSerializer):
    """ Favorite List Serializer """
    content_object = FavoriteObjectRelatedField(read_only=True)

    class Meta:
        model = Favorite
        fields = [
            'uuid',
            'content_object',
            'created_at',
        ]


class ReviewListCreateSerializer(serializers.ModelSerializer):
    """ Review List Create Serializer """
    user = serializers.PrimaryKeyRelatedField(
        write_only=True,
        required=False,
        queryset=UserModel.objects.all(),
    )
    author = UserShortReadSerializer(read_only=True)

    def create(self, validated_data):
        try:
            instance = Review.objects.create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'create': _('You have already left a review here.')})
        return instance

    class Meta:
        model = Review
        fields = [
            'uuid',
            'user',
            'author',
            'rating',
            'comment',
            'created_at',
        ]


class ReviewRUDSerializer(serializers.ModelSerializer):
    """ Review Retrieve Update Destroy Serializer """

    class Meta:
        model = Review
        fields = [
            'uuid',
            'rating',
            'comment',
        ]


class CommentListCreateSerializer(serializers.ModelSerializer):
    """ Comment List Create Serializer """
    author = UserShortReadSerializer(read_only=True)

    def get_fields(self):
        fields = super().get_fields()
        fields['comments'] = CommentListCreateSerializer(
            read_only=True,
            many=True,
        )
        return fields

    class Meta:
        model = Comment
        fields = [
            'uuid',
            'author',
            'content',
            'created_at',
            'comments',
        ]


class CommentRUDSerializer(serializers.ModelSerializer):
    """ Comment Retrieve Update Destroy Serializer """

    class Meta:
        model = Comment
        fields = [
            'uuid',
            'content',
        ]
