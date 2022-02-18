from rest_framework import serializers
from .models import MWUser, Organizer


class MWUserSerializer(serializers.ModelSerializer):
    """ MWUser Serializer """

    class Meta:
        model = MWUser
        fields = [
            'name',
            'avatar',
        ]


class OrganizerSerializer(serializers.ModelSerializer):
    """ Organizer Serializer """
    user = MWUserSerializer()

    class Meta:
        model = MWUser
        fields = [
            'user',
        ]
