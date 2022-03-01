from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import ugettext_lazy as _
from main.serializers import (
    CountrySerializer,
    CitySerializer,
    LanguageSerializer,
)
from .choices import UserType
from .models import Customer, Organizer
from .serializer_fields import (
    UserSerializerField,
    UserDetailSerializerField,
    OrganizerLinkSerializerField,
)


UserModel = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """ Registration Serializer """
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = [
            'username',
            'email',
            'password',
            'password2',
            'user_type',
            'name',
        ]
        extra_kwargs = {
            'user_type': {'choices': UserType.choices[1:]},
            'name': {'required': True},
        }

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError(_('This field may not be blank.'))
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({
                'password': _('Password fields did not match.')})
        return data

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data['user_type'],
            name=validated_data['name'],
        )

        if user.user_type == UserType.CUSTOMER:
            Customer.objects.create(user=user)
        elif user.user_type == UserType.ORGANIZER:
            Organizer.objects.create(user=user)

        return user


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
