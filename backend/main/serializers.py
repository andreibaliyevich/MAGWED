from rest_framework import serializers
from .models import Country, City, Language


class CountryListSerializer(serializers.ModelSerializer):
    """ Country List Serializer """

    class Meta:
        model = Country
        fields = [
            'code',
            'name',
            'name_local',
        ]


class CityListSerializer(serializers.ModelSerializer):
    """ City List Serializer """

    class Meta:
        model = City
        fields = [
            'slug',
            'name',
            'name_local',
        ]


class LanguageListSerializer(serializers.ModelSerializer):
    """ Language List Serializer """

    class Meta:
        model = Language
        fields = [
            'code',
            'name',
            'name_local',
        ]
