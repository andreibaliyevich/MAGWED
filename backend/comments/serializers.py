from rest_framework import serializers
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _
from accounts.serializers import UserShortReadSerializer
from blog.models import Article
from portfolio.models import Album, Photo
from .models import Comment


class CommentListCreateSerializer(serializers.ModelSerializer):
    """ Comment List Create Serializer """
    content_type = serializers.CharField(write_only=True)
    object_uuid = serializers.UUIDField(write_only=True)
    author = UserShortReadSerializer(read_only=True)

    def get_fields(self):
        fields = super().get_fields()
        fields['comments'] = CommentListCreateSerializer(
            read_only=True,
            many=True,
        )
        return fields

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
                'content_type': _('Invalid content_type.')})

        try:
            self.content_object = object_class.objects.get(
                uuid=data['object_uuid'])
        except object_class.DoesNotExist:
            raise serializers.ValidationError({
                'object_uuid': _('Object does not exist.')})

        return data

    def create(self, validated_data):
        try:
            comment = Comment.objects.create(
                author=self.context['request'].user,
                content_object=self.content_object,
                content=validated_data['content'],
            )
        except IntegrityError:
            raise serializers.ValidationError({
                'create': _('You have already commented here.')})
        return comment

    class Meta:
        model = Comment
        fields = [
            'uuid',
            'content_type',
            'object_uuid',
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
