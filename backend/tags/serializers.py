from rest_framework import serializers
from .models import Tag


class TagListSerializer(serializers.ModelSerializer):
    """ Tag Serializer """

    class Meta:
        model = Tag
        fields = [
            'name',
            'slug',
        ]