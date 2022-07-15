from rest_framework import serializers
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _
from accounts.serializers import UserShortReadSerializer
from blog.models import Article
from portfolio.models import Album, Photo
from .models import Notification, Comment
from .serializer_fields import ContentObjectRelatedField


class NotificationListSerializer(serializers.ModelSerializer):
    """ Notification List Serializer """
    content_object = ContentObjectRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'content_object',
            'viewed',
            'created_at',
        ]


class CommentReadSerializer(serializers.ModelSerializer):
    """ Comment Read Serializer """
    user = UserShortReadSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'content',
            'created_at',
            'comments',
        ]

    def get_fields(self):
        fields = super().get_fields()
        fields['comments'] = CommentListSerializerField(
            read_only=True,
            many=True,
        )
        return fields


class CommentCreateSerializer(serializers.ModelSerializer):
    """ Comment Create Serializer """
    content_type = serializers.CharField(write_only=True)
    object_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'content_type',
            'object_id',
            'content',
            'created_at',
        ]

    def validate(self, data):
        if data['content_type'] == 'article':
            object_class = Article
        elif data['content_type'] == 'album':
            object_class = Album
        elif data['content_type'] == 'photo':
            object_class = Photo
        elif data['content_type'] == 'comment':
            object_class = Comment
        else:
            raise serializers.ValidationError({
                'content_type': _('Invalid object type.')})

        try:
            self.content_object = object_class.objects.get(id=data['object_id'])
        except object_class.DoesNotExist:
            raise serializers.ValidationError({
                'object_id': _('Object does not exist.')})

        return data

    def create(self, validated_data):
        try:
            comment = Comment.objects.create(
                user=self.context['request'].user,
                content_object=self.content_object,
                content=validated_data['content'],
            )
        except IntegrityError:
            raise serializers.ValidationError({
                'create': _('You have already left a comment here.')})
        return comment
