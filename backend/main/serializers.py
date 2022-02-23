from rest_framework import serializers
from .models import Country, City, Language, Hashtag


class CountrySerializer(serializers.ModelSerializer):
    """ Country Serializer """

    class Meta:
        model = Country
        fields = [
            'code',
            'name',
            'name_local',
        ]


class CitySerializer(serializers.ModelSerializer):
    """ City Serializer """

    class Meta:
        model = City
        fields = [
            'slug',
            'name',
            'name_local',
        ]


class LanguageSerializer(serializers.ModelSerializer):
    """ Language Serializer """

    class Meta:
        model = Language
        fields = [
            'code',
            'name',
            'name_local',
        ]


class HashtagSerializer(serializers.ModelSerializer):
    """ Hashtag Serializer """

    class Meta:
        model = Hashtag
        fields = [
            'name',
            'slug',
        ]
