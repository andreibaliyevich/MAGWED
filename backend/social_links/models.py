from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from .choices import LinkType


class SocialLink(models.Model):
    """ Social Link Model """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='social_links',
        verbose_name=_('User'),
    )

    link_type = models.PositiveSmallIntegerField(
        choices=LinkType.choices,
        verbose_name=_('Type of Link'),
    )
    link_url = models.URLField(verbose_name=_('URL of Link'))

    class Meta:
        verbose_name = _('Social Link')
        verbose_name_plural = _('Social Links')
        ordering = ['user', 'id']
