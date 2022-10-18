from easy_thumbnails.fields import ThumbnailerImageField
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from .utilities import get_magazine_path
from .validators import MinimumImageSizeValidator


class Country(models.Model):
    """ Country Model """
    code = models.SlugField(
        max_length=2,
        primary_key=True,
        verbose_name=_('Code'),
    )
    name = models.CharField(max_length=64, verbose_name=_('Name'))
    name_local = models.CharField(max_length=64, verbose_name=_('Name (local)'))

    def __str__(self):
        return f'{ self.name_local } ({ self.name })'

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        ordering = ['name', 'code']


class City(models.Model):
    """ City Model """
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name='cities',
        verbose_name=_('Country'),
    )
    name = models.CharField(max_length=64, verbose_name=_('Name'))
    name_local = models.CharField(max_length=64, verbose_name=_('Name (local)'))

    def __str__(self):
        return f'{ self.name_local } ({ self.name })'

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')
        ordering = ['name', 'country']


class Language(models.Model):
    """ Language Model """
    code = models.SlugField(
        max_length=2,
        primary_key=True,
        verbose_name=_('Code'),
    )
    name = models.CharField(max_length=64, verbose_name=_('Name'))
    name_local = models.CharField(max_length=64, verbose_name=_('Name (local)'))

    def __str__(self):
        return f'{ self.name_local } ({ self.name })'

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')
        ordering = ['name', 'code']


class Hashtag(models.Model):
    """ Hashtag Model """
    name = models.CharField(max_length=64, unique=True, verbose_name=_('Name'))
    slug = models.SlugField(max_length=64, unique=True, verbose_name=_('Slug'))

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Hashtag')
        verbose_name_plural = _('Hashtags')
        ordering = ['-created_at', '-id']


class Magazine(models.Model):
    """ Magazine Model """
    title = models.CharField(max_length=128, verbose_name=_('Title'))
    slug = models.SlugField(max_length=64, unique=True, verbose_name=_('Slug'))

    image = ThumbnailerImageField(
        upload_to=get_magazine_path,
        validators=[
            FileExtensionValidator(allowed_extensions=('jpg', 'png')),
            MinimumImageSizeValidator(500, 650),
        ],
        resize_source={
            'size': (500, 650),
            'crop': 'smart',
            'autocrop': True,
            'quality': 100,
        },
        help_text=_(
            'Upload JPG or PNG image. '
            'Required minimum of size %(width)d x %(height)d.'
        ) % {
            'width': 500,
            'height': 650,
        },
        verbose_name=_('Image'),
    )
    file = models.FileField(
        upload_to=get_magazine_path,
        validators=[
            FileExtensionValidator(allowed_extensions=('pdf',)),
        ],
        verbose_name=_('File'),
    )

    published_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Published at'),
    )

    def __str__(self):
        return f'{ self.title } | { self.published_at }'

    class Meta:
        verbose_name = _('Magazine')
        verbose_name_plural = _('Magazines')
        ordering = ['-published_at', '-id']
