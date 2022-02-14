from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import (
    GenericRelation,
    GenericForeignKey,
)
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    """ Notification Model """
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )

    viewed = models.BooleanField(default=False, verbose_name=_('Viewed'))
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-created_at', '-id']
        unique_together = ['content_type', 'object_id', 'user']


class Follow(models.Model):
    """ Follow Model """
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name=_('Follower'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name=_('User'),
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )

    class Meta:
        verbose_name = _('Follow object')
        verbose_name_plural = _('Follow objects')
        ordering = ['-created_at', '-id']
        unique_together = ['follower', 'user']


class Favorite(models.Model):
    """ Favorite Model """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )

    class Meta:
        verbose_name = _('Favorite')
        verbose_name_plural = _('Favorites')
        ordering = ['-created_at', '-id']
        unique_together = ['user', 'content_type', 'object_id']


class Comment(models.Model):
    """ Comment Model """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    content = models.CharField(max_length=255, verbose_name=_('Content'))
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )

    comments = GenericRelation('self')

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['created_at', 'id']
        unique_together = ['user', 'content_type', 'object_id']


class Review(models.Model):
    """ Review Model """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_reviews',
        verbose_name=_('User'),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='author_reviews',
        verbose_name=_('Author'),
    )

    class ReviewChoices(models.IntegerChoices):
        FIVE = 5, _('5 stars')
        FOUR = 4, _('4 stars')
        THREE = 3, _('3 stars')
        TWO = 2, _('2 stars')
        ONE = 1, _('1 star')

        __empty__ = _('Choose rating')

    rating = models.IntegerField(
        choices=ReviewChoices.choices,
        verbose_name=_('Rating'),
    )

    comment = models.TextField(verbose_name=_('Comment'))
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )

    class Meta:
        verbose_name = _('Review')
        verbose_name_plural = _('Reviews')
        ordering = ['-created_at', '-id']
        unique_together = ['user', 'author']
