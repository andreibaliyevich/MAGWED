from rest_framework import serializers
from .models import Organizer
from .serializer_fields import (
    UserSerializerField,
    UserDetailSerializerField,
    OrganizerLinkSerializerField,
)


class OrganizerListSerializer(serializers.ModelSerializer):
    """ Organizer List Serializer """
    user = UserSerializerField(read_only=True)
    organizerlink_set = OrganizerLinkSerializerField(read_only=True, many=True)

    class Meta:
        model = Organizer
        fields = [
            'user',
            'profile_url',
            'organizerlink_set',
        ]


class OrganizerDetailSerializer(serializers.ModelSerializer):
    """ Organizer Detail Serializer """
    user = UserDetailSerializerField(read_only=True)
    organizerlink_set = OrganizerLinkSerializerField(read_only=True, many=True)

    class Meta:
        model = Organizer
        fields = [
            'roles',
            'user',
            'cover',
            'description',
            'countries',
            'cities',
            'languages',
            'cost_work',
            'number_hours',
            'rating',
            'profile_url',
            'organizerlink_set',
        ]