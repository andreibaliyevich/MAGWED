from rest_framework import serializers
from .models import Hashtag


class HashtagSerializerField(serializers.ModelSerializer):
    """ HashtagSerializerField """

    class Meta:
        model = Hashtag
        fields = [
            'name',
            'slug',
        ]
