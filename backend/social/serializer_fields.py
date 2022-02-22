from rest_framework import serializers
from accounts.models import MWUser
from accounts.serializer_fields import UserSerializerField
from portfolio.models import Album, Photo
from portfolio.serializer_fields import (
    AlbumSerializerField,
    PhotoSerializerField,
)
from .models import Comment


class ContentObjectRelatedField(serializers.RelatedField):
    """
    A custom field to use for the 'content_object' generic relationship.
    """

    def to_representation(self, value):
        if isinstance(value, MWUser):
            serializer = UserSerializerField(value)
        elif isinstance(value, Album):
            serializer = AlbumSerializerField(value)
        elif isinstance(value, Photo):
            serializer = PhotoSerializerField(value)
        else:
            raise Exception('Unexpected type of content object')
        return serializer.data


class CommentListSerializerField(serializers.ModelSerializer):
    """ Comment List Serializer Field """
    user = UserSerializerField(read_only=True)

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
