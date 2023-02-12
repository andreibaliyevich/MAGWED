from rest_framework import serializers
from .models import SocialLink


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
