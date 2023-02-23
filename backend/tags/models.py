import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Tag(models.Model):
    """ Tag Model """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(unique=True, max_length=64, verbose_name=_('Name'))
    slug = models.SlugField(unique=True, max_length=64, verbose_name=_('Slug'))

    created_at = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name=_('Created at'),
    )

    def __str__(self):
        return f'{ self.name } ({ self.slug })'

    def save(self, *args, **kwargs):
        if self._state.adding:
            slug = self.slugify(self.name)
            slugs = set(
                type(self)
                ._default_manager.filter(slug__startswith=self.slug)
                .values_list('slug', flat=True)
            )

            if slug in slugs:
                i = 1
                while True:
                    slug = self.slugify(self.name, i)
                    if slug not in slugs:
                        self.slug = slug
                        break
                    i += 1
            else:
                self.slug = slug

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['-created_at']


class TaggedItem(models.Model):
    """ Tagged Item Model """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        related_name='tagged_items',
        verbose_name=_('Tag'),
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_uuid = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_uuid')

    created_at = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name=_('Created at'),
    )

    def __str__(self):
        return f'{ self.tag } | { self.content_object }'

    class Meta:
        verbose_name = _('Tagged Item')
        verbose_name_plural = _('Tagged Items')
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['tag', 'content_type', 'object_uuid'],
                name='unique_taggeditem',
            )
        ]
        indexes = [
            models.Index(fields=['content_type', 'object_uuid']),
        ]
