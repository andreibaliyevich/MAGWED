from rest_framework import serializers
from .models import MWUser, Organizer


class UserSerializerField(serializers.ModelSerializer):
    """ User Serializer Field """

    class Meta:
        model = MWUser
        fields = [
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

    class Meta:
        model = MWUser
        fields = [
            'email',
            'name',
            'avatar',
            'country',
            'city',
            'phone',
            'last_visit',
        ]
