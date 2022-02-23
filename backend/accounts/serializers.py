from rest_framework import serializers
from main.serializers import (
    CountrySerializer,
    CitySerializer,
    LanguageSerializer,
)
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
    countries = CountrySerializer(read_only=True, many=True)
    cities = CitySerializer(read_only=True, many=True)
    languages = LanguageSerializer(read_only=True, many=True)
    organizerlink_set = OrganizerLinkSerializerField(read_only=True, many=True)

    class Meta:
        model = Organizer
        fields = [
            'user',
            'roles',
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
