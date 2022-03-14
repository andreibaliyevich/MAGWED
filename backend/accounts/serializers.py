from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
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
            Organizer.objects.create(user=user, profile_url=user.username)

        self.send_activation_email(user)
        return user

    def send_activation_email(self, user):
        context = {
            'SITE_NAME': settings.SITE_NAME,
            'SITE_HOST': settings.SITE_HOST,
            'uid': force_str(urlsafe_base64_encode(force_bytes(user.pk))),
            'token': default_token_generator.make_token(user),
        }

        subject = render_to_string('email/activation_subject.txt')
        text_content = render_to_string('email/activation_text.html', context)
        html_content = render_to_string('email/activation_html.html', context)

        user.email_user(
            subject=subject,
            message=text_content,
            from_email=settings.EMAIL_HOST_USER,
            html_message=html_content,
        )


class ActivationSerializer(serializers.Serializer):
    """ Activation Serializer """
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):
        try:
            pk = force_str(urlsafe_base64_decode(data['uid']))
            self.user = UserModel.objects.get(pk=pk)
        except (UserModel.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {'uid': _('Invalid user id or user does not exist.')},
                code='invalid_uid',
            )

        if default_token_generator.check_token(self.user, data['token']):
            return data
        else:
            raise serializers.ValidationError(
                {'token': _('Invalid token for given user.')},
                code='invalid_token',
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
