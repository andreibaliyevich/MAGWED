from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _
from accounts.serializers import UserShortReadSerializer
from .models import SocialLink, Follow, Comment, Review


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


class FollowSerializer(serializers.Serializer):
    """ Follow Serializer """
    uuid = serializers.UUIDField()

    def validate_uuid(self, value):
        try:
            self.user = UserModel.objects.get(uuid=value)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError(
                _('User with given uuid does not exist.'))
        return value


class FollowingSerializer(serializers.ModelSerializer):
    """ Following Serializer """
    user = UserShortReadSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = [
            'user',
            'created_at',
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


class ReviewListCreateSerializer(serializers.ModelSerializer):
    """ Review List Create Serializer """
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
