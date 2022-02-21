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
    """ Organizer Serializer """
    user = UserSerializerField(read_only=True)

    class Meta:
        model = Organizer
        fields = [
            'user',
        ]
