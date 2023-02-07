from rest_framework import serializers
from .models import OrganizerLink


class SocialLinkSerializer(serializers.ModelSerializer):
    """ Social Link Serializer """

    class Meta:
        model = OrganizerLink
        fields = [
            'id',
            'link_type',
            'link_url',
        ]


class SocialLinkReadSerializer(serializers.ModelSerializer):
    """ Social Link Read Serializer """

    class Meta:
        model = OrganizerLink
        fields = [
            'link_type',
            'link_url',
        ]
