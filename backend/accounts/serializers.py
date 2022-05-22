from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _
from main.models import Country, City, Language
from main.serializers import (
    CountrySerializer,
    CitySerializer,
    LanguageSerializer,
)
from .choices import UserType
from .models import Customer, OrganizerRole, Organizer
from .serializer_fields import (
    UserSerializerField,
    UserDetailSerializerField,
    OrganizerLinkSerializerField,
)


UserModel = get_user_model()


class UserLoginSerializer(serializers.ModelSerializer):
    """ User Login Serializer """

    class Meta:
        model = UserModel
        fields = [
            'username',
            'user_type',
            'avatar',
        ]


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
        }

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


class UidAndTokenSerializer(serializers.Serializer):
    """ Uid and Token Serializer """
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

        if not default_token_generator.check_token(self.user, data['token']):
            raise serializers.ValidationError(
                {'token': _('Invalid token for given user.')},
                code='invalid_token',
            )

        return data


class PasswordChangeSerializer(serializers.Serializer):
    """ Password Change Serializer """
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
    )
    new_password2 = serializers.CharField(write_only=True)

    def validate_current_password(self, value):
        if not self.context['user'].check_password(value):
            raise serializers.ValidationError(_('Invalid current password.'))
        return value

    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError({
                'new_password': _('Password fields did not match.')})
        return data


class PasswordResetSerializer(serializers.Serializer):
    """ Password Reset Serializer """
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            self.user = UserModel.objects.get(email=value, is_active=True)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError(
                _('User with given email does not exist.'))
        return value

    def send_password_reset_email(self):
        context = {
            'SITE_NAME': settings.SITE_NAME,
            'SITE_HOST': settings.SITE_HOST,
            'uid': force_str(urlsafe_base64_encode(force_bytes(self.user.pk))),
            'token': default_token_generator.make_token(self.user),
        }

        subject = render_to_string('email/password_reset_subject.txt')
        text_content = render_to_string(
            'email/password_reset_text.html', context)
        html_content = render_to_string(
            'email/password_reset_html.html', context)

        self.user.email_user(
            subject=subject,
            message=text_content,
            from_email=settings.EMAIL_HOST_USER,
            html_message=html_content,
        )


class PasswordResetConfirmSerializer(serializers.Serializer):
    """ Password Reset Confirm Serializer """
    uid = serializers.CharField()
    token = serializers.CharField()

    new_password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
    )
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            pk = force_str(urlsafe_base64_decode(data['uid']))
            self.user = UserModel.objects.get(pk=pk)
        except (UserModel.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {'uid': _('Invalid user id or user does not exist.')},
                code='invalid_uid',
            )

        if not default_token_generator.check_token(self.user, data['token']):
            raise serializers.ValidationError(
                {'token': _('Invalid token for given user.')},
                code='invalid_token',
            )

        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError({
                'new_password': _('Password fields did not match.')})

        return data


class UserProfileSerializer(serializers.ModelSerializer):
    """ User Profile Serializer """
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), allow_null=True)
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), allow_null=True)

    class Meta:
        model = UserModel
        fields = [
            'name',
            'country',
            'city',
            'phone',
        ]


class CustomerProfileSerializer(serializers.ModelSerializer):
    """ Customer Profile Serializer """
    user = UserProfileSerializer()

    class Meta:
        model = Customer
        fields = [
            'user',
            'date_of_wedding',
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        user.name = user_data.get('name', user.name)
        user.country = user_data.get('country', user.country)
        user.city = user_data.get('city', user.city)
        user.phone = user_data.get('phone', user.phone)
        user.save()

        instance.date_of_wedding = validated_data.get(
            'date_of_wedding', instance.date_of_wedding)
        instance.save()

        return instance


class OrganizerProfileSerializer(serializers.ModelSerializer):
    """ Organizer Profile Serializer """
    user = UserProfileSerializer()
    roles = serializers.PrimaryKeyRelatedField(
        queryset=OrganizerRole.objects.all(), many=True)
    cover = serializers.ImageField(read_only=True)
    countries = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.all(), many=True)
    cities = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), many=True)
    languages = serializers.PrimaryKeyRelatedField(
        queryset=Language.objects.all(), many=True)
    rating = serializers.DecimalField(
        max_digits=2, decimal_places=1, read_only=True)
    pro_time = serializers.DateTimeField(read_only=True)

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
            'profile_url',
            'rating',
            'pro_time',
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        user.name = user_data.get('name', user.name)
        user.country = user_data.get('country', user.country)
        user.city = user_data.get('city', user.city)
        user.phone = user_data.get('phone', user.phone)
        user.save()

        instance.roles.set(validated_data.get('roles', instance.roles))
        instance.description = validated_data.get(
            'description', instance.description)
        instance.countries.set(
            validated_data.get('countries', instance.countries))
        instance.cities.set(validated_data.get('cities', instance.cities))
        instance.languages.set(
            validated_data.get('languages', instance.languages))
        instance.cost_work = validated_data.get(
            'cost_work', instance.cost_work)
        instance.number_hours = validated_data.get(
            'number_hours', instance.number_hours)
        instance.profile_url = validated_data.get(
            'profile_url', instance.profile_url)
        instance.save()

        return instance


class AvatarProfileSerializer(serializers.ModelSerializer):
    """ Avatar Profile Serializer """

    class Meta:
        model = UserModel
        fields = ['avatar']


class CoverOrganizerSerializer(serializers.ModelSerializer):
    """ Cover Organizer Serializer """

    class Meta:
        model = Organizer
        fields = ['cover']


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
