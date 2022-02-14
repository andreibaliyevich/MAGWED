from easy_thumbnails.fields import ThumbnailerImageField
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Avg, Value
from django.db.models.functions import Coalesce
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from main.models import Country, City, Language
from main.utilities import get_cover_path
from social.models import Review
from .managers import MWUserManager
from .utilities import get_avatar_path


class MWUser(AbstractBaseUser, PermissionsMixin):
    """ User Model """

    class UserType(models.IntegerChoices):
        ADMIN = 1, _('Administrator')
        CUSTOMER = 2, _('Customer')
        ORGANIZER = 3, _('Organizer')

    user_type = models.IntegerField(
        choices=UserType.choices,
        default=UserType.CUSTOMER,
        verbose_name=_('User type'),
    )

    email = models.EmailField(unique=True, verbose_name=_('Email address'))

    name = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('Name'),
    )
    avatar = ThumbnailerImageField(
        null=True,
        blank=True,
        upload_to=get_avatar_path,
        resize_source={
            'size': (512, 512),
            'crop': 'smart',
            'autocrop': True,
            'quality': 100,
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

    is_active = models.BooleanField(default=False, verbose_name=_('Active'))
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('Staff status'),
    )
    is_superuser = models.BooleanField(
        default=False,
        verbose_name=_('Superuser status'),
    )

    last_visit = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Last visit'),
    )
    last_login = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Last login'),
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Date joined'),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MWUserManager()

    def __str__(self):
        return self.email

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

    class RoleChoices(models.IntegerChoices):
        PHOTOGRAPHER = 1, _('Photographer')
        VIDEOGRAPHER = 2, _('Videographer')
        LEADING = 3, _('Leading')
        MUSICIAN = 4, _('Musician')
        DJ = 5, _('DJ')
        AGENCY = 6, _('Agency')
        SALON = 7, _('Salon')
        CONFECTIONERY = 8, _('Confectionery')
        DECORATOR = 9, _('Decorator')
        VISAGISTE = 10, _('Visagiste')
        HAIRDRESSER = 11, _('Hairdresser')

        __empty__ = _('(Unknown)')

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
        verbose_name=_('Roles'),
    )

    cover = models.ImageField(
        null=True,
        blank=True,
        upload_to=get_cover_path,
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

    def get_absolute_url(self):
        return reverse('accounts:organizer_detail', args=[self.profile_url])

    class Meta:
        verbose_name = _('Organizer')
        verbose_name_plural = _('Organizers')
        ordering = ['user']


class UserLink(models.Model):
    """ User Link Model """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
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
        verbose_name = _('Link of User')
        verbose_name_plural = _('Links of User')
        ordering = ['user', 'id']


@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_organizer_rating(sender, **kwargs):
    """ Update rating of organizer """
    user = kwargs['instance'].user
    organizer_rating = user.user_reviews.aggregate(
        total_rating=Coalesce(Avg('rating'), Value(0.0)))
    user.organizer.rating = organizer_rating['total_rating']
    user.organizer.save()
