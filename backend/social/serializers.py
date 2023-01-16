from rest_framework import serializers
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _
from accounts.serializers import UserShortReadSerializer
from .models import Comment, Review


class CommentListCreateSerializer(serializers.ModelSerializer):
    """ Comment List Create Serializer """
    author = UserShortReadSerializer(read_only=True)

    def get_fields(self):
        fields = super().get_fields()
        fields['comments'] = CommentListCreateSerializer(
            read_only=True, many=True)
        return fields

    class Meta:
        model = Comment
        fields = [
            'id',
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
            'id',
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
            'id',
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
            'id',
            'rating',
            'comment',
        ]
