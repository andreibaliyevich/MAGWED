import uuid
from contextlib import suppress
from exif import Image as ExifImage
from easy_thumbnails.fields import ThumbnailerImageField
from django.conf import settings
from django.core.files import File
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from main.models import Hashtag
from main.utilities import get_cover_path, get_thumbnail_path
from .utilities import get_photo_path


class Album(models.Model):
    """ Album Model """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='albums',
        verbose_name=_('Owner'),
    )

    image = models.ImageField(upload_to=get_cover_path, verbose_name=_('Image'))
    thumbnail = ThumbnailerImageField(
        upload_to=get_thumbnail_path,
        resize_source={
            'size': (800, 800),
            'crop': 'smart',
            'autocrop': True,
            'quality': 100,
        },
        verbose_name=_('Thumbnail'),
    )

    title = models.CharField(max_length=128, verbose_name=_('Title'))
    description = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('Description'),
    )
    hashtags = models.ManyToManyField(
        Hashtag,
        blank=True,
        verbose_name=_('Hashtags'),
    )

    created_at = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name=_('Created at'),
    )

    num_views = models.IntegerField(
        default=0,
        verbose_name=_('Number of views'),
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='album_likes',
        verbose_name=_('Likes'),
    )
    rating = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Rating'),
    )

    def save(self, *args, **kwargs):
        self.thumbnail = File(self.image)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Album')
        verbose_name_plural = _('Albums')
        ordering = ['-created_at']


class Photo(models.Model):
    """ Photo Model """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='photos',
        verbose_name=_('Owner'),
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='photos',
        verbose_name=_('Album'),
    )

    image = models.ImageField(upload_to=get_photo_path, verbose_name=_('Image'))
    thumbnail = ThumbnailerImageField(
        upload_to=get_thumbnail_path,
        resize_source={
            'size': (800, 800),
            'crop': 'smart',
            'autocrop': True,
            'quality': 100,
        },
        verbose_name=_('Thumbnail'),
    )

    device = models.CharField(
        blank=True,
        max_length=128,
        verbose_name=_('Device'),
    )
    f_number = models.DecimalField(
        blank=True,
        null=True,
        max_digits=5,
        decimal_places=2,
        verbose_name=_('F-number (f/)'),
    )
    exposure_time = models.CharField(
        blank=True,
        max_length=32,
        validators=[
            RegexValidator(
                regex=r'^\d\/\d{1,9}$',
                message=_('Must be entered in the format: 1/123456789.')
            ),
        ],
        verbose_name=_('Exposure time (s)'),
    )
    focal_length = models.DecimalField(
        blank=True,
        null=True,
        max_digits=5,
        decimal_places=2,
        verbose_name=_('Focal length (mm)'),
    )
    photographic_sensitivity = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        verbose_name=_('Photographic sensitivity (ISO)'),
    )

    title = models.CharField(
        blank=True,
        max_length=128,
        verbose_name=_('Title'),
    )
    description = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('Description'),
    )
    hashtags = models.ManyToManyField(
        Hashtag,
        blank=True,
        verbose_name=_('Hashtags'),
    )

    uploaded_at = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name=_('Uploaded at'),
    )

    num_views = models.IntegerField(
        default=0,
        verbose_name=_('Number of views'),
    )
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='photo_likes',
        verbose_name=_('Likes'),
    )
    rating = models.PositiveIntegerField(
        default=0,
        verbose_name=_('Rating'),
    )

    def save(self, *args, **kwargs):
        self.thumbnail = File(self.image)

        exif_img = ExifImage(self.image)
        with suppress(Exception):
            self.device = f'{ exif_img.make } { exif_img.model }'
        with suppress(Exception):
            self.f_number = exif_img.f_number
        with suppress(Exception):
            self.exposure_time = f'1/{ int(1 / float(exif_img.exposure_time)) }'
        with suppress(Exception):
            self.focal_length = exif_img.focal_length
        with suppress(Exception):
            self.photographic_sensitivity = exif_img.photographic_sensitivity

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')
        ordering = ['-uploaded_at']
