from easy_thumbnails.fields import ThumbnailerImageField
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.mail import send_mail
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from main.models import Country, City, Language
from main.utilities import get_cover_path
from .choices import UserType, RoleChoices
from .managers import MWUserManager
from .utilities import get_avatar_path
from .validators import MinimumImageSizeValidator


class MWUser(AbstractBaseUser, PermissionsMixin):
    """ User Model """
    username_validator = ASCIIUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
        help_text=_(
            'Required. 150 characters or fewer. '
            'Letters, digits and @/./+/-/_ only.'
        ),
        verbose_name=_('Username'),
    )
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': _('A user with that email address already exists.'),
        },
        verbose_name=_('Email address'),
    )

    user_type = models.IntegerField(
        choices=UserType.choices,
        verbose_name=_('User type'),
    )

    name = models.CharField(blank=True, max_length=255, verbose_name=_('Name'))
    avatar = ThumbnailerImageField(
        null=True,
        blank=True,
        upload_to=get_avatar_path,
        validators=[
            FileExtensionValidator(allowed_extensions=('jpg', 'png')),
            MinimumImageSizeValidator(800, 800),
        ],
        resize_source={
            'size': (800, 800),
            'crop': 'smart',
            'autocrop': True,
            'quality': 100,
        },
        help_text=_(
            'Upload JPG or PNG image. '
            'Required minimum of size %(width)d x %(height)d.'
        ) % {
            'width': 800,
            'height': 800,
        },
        verbose_name=_('Avatar'),
    )

    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name=_('Country'),
    )
    city = models.ForeignKey(
        City,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name=_('City'),
    )
    phone = models.CharField(
        blank=True,
        max_length=21,
        validators=[
            RegexValidator(
                regex=r'^(\s*)?(\+)?([- _():=+]?\d[- _():=+]?){9,16}(\s*)?$',
                message=_('Wrong format!'),
            ),
        ],
        verbose_name=_('Phone'),
    )

    is_staff = models.BooleanField(
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'
        ),
        verbose_name=_('Staff status'),
    )
    is_active = models.BooleanField(
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
        verbose_name=_('Active'),
    )

    last_visit = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Last visit'),
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Date joined'),
    )

    objects = MWUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f'{ self.username } | { self.email }'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """ Send an email to this user. """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['email']


class Customer(models.Model):
    """ Customer Model """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name=_('User'),
    )
    date_of_wedding = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Date of Wedding'),
    )

    class Meta:
        verbose_name = _('Customer')
        verbose_name_plural = _('Customers')
        ordering = ['user']


class OrganizerRole(models.Model):
    """ Role of Organizer Model """
    role_id = models.PositiveSmallIntegerField(
        choices=RoleChoices.choices,
        primary_key=True,
        verbose_name=_('Identifier'),
    )

    def __str__(self):
        return self.get_role_id_display()

    class Meta:
        verbose_name = _('Role of Organizer')
        verbose_name_plural = _('Roles of Organizers')
        ordering = ['role_id']


class Organizer(models.Model):
    """ Organizer Model """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name=_('User'),
    )
    roles = models.ManyToManyField(
        OrganizerRole,
        blank=True,
        verbose_name=_('Roles'),
    )

    cover = models.ImageField(
        null=True,
        blank=True,
        upload_to=get_cover_path,
        validators=[
            FileExtensionValidator(allowed_extensions=('jpg', 'png')),
            MinimumImageSizeValidator(1900, 1200),
        ],
        help_text=_(
            'Upload JPG or PNG image. '
            'Required minimum of size %(width)d x %(height)d.'
        ) % {
            'width': 1900,
            'height': 1200,
        },
        verbose_name=_('Cover'),
    )
    description = models.TextField(blank=True, verbose_name=_('Description'))

    countries = models.ManyToManyField(
        Country,
        blank=True,
        verbose_name=_('Countries'),
    )
    cities = models.ManyToManyField(
        City,
        blank=True,
        verbose_name=_('Cities'),
    )
    languages = models.ManyToManyField(
        Language,
        blank=True,
        verbose_name=_('Languages'),
    )

    cost_work = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0.0,
        verbose_name=_('Cost of work'),
        help_text=_('Please enter in USD ($)'),
    )
    number_hours = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Number of hours'),
    )

    profile_url = models.SlugField(
        max_length=64,
        unique=True,
        verbose_name=_('Profile URL'),
    )

    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0.0,
        verbose_name=_('Rating'),
    )
    pro_time = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Pro-account valid time'),
    )

    class Meta:
        verbose_name = _('Organizer')
        verbose_name_plural = _('Organizers')
        ordering = ['user']


class OrganizerLink(models.Model):
    """ Organizer Link Model """
    organizer = models.ForeignKey(
        Organizer,
        on_delete=models.CASCADE,
        verbose_name=_('Organizer'),
    )

    class LinkType(models.TextChoices):
        WEBSITE = 'WE', _('Website')
        INSTAGRAM = 'IM', _('Instagram')
        FACEBOOK = 'FK', _('Facebook')
        TWITTER = 'TR', _('Twitter')
        PINTEREST = 'PT', _('Pinterest')
        VK = 'VK', _('VK')

    link_type = models.CharField(
        max_length=2,
        choices=LinkType.choices,
        default=LinkType.WEBSITE,
        verbose_name=_('Type of Link'),
    )

    link_url = models.URLField(verbose_name=_('URL of Link'))

    class Meta:
        verbose_name = _('Link of Organizer')
        verbose_name_plural = _('Links of Organizer')
        ordering = ['organizer', 'id']
