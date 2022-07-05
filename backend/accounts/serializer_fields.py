from rest_framework import serializers
from django.contrib.auth import get_user_model
from main.serializers import CountrySerializer, CitySerializer
from .models import Organizer, OrganizerLink


UserModel = get_user_model()


class UserSerializerField(serializers.ModelSerializer):
    """ User Serializer Field """

    class Meta:
        model = UserModel
        fields = [
            'id',
            'name',
            'avatar',
        ]


class OrganizerSerializerField(serializers.ModelSerializer):
    """ Organizer Serializer Field """
    user = UserSerializerField(read_only=True)

    class Meta:
        model = Organizer
        fields = [
            'user',
            'profile_url',
        ]


class UserDetailSerializerField(serializers.ModelSerializer):
    """ User Detail Serializer Field """
    country = CountrySerializer(read_only=True)
    city = CitySerializer(read_only=True)

    class Meta:
        model = UserModel
        fields = [
            'email',
            'name',
            'avatar',
            'country',
            'city',
            'phone',
            'last_visit',
        ]


class OrganizerLinkSerializerField(serializers.ModelSerializer):
    """ Organizer Link Serializer Field """

    class Meta:
        model = OrganizerLink
        fields = [
            'link_type',
            'link_url',
        ]
