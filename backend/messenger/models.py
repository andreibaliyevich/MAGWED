from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Chat(models.Model):
    """ Chat Model """
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Members'),
    )

    last_message = models.OneToOneField(
        'Message',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='last_message',
        verbose_name=_('Last message'),
    )

    def get_absolute_url(self):
        return reverse('messenger:chat_detail', args=[self.id])

    class Meta:
        verbose_name = _('Chat')
        verbose_name_plural = _('Chats')
        ordering = ['-last_message__created_at', '-id']


class Message(models.Model):
    """ Message Model """
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        verbose_name=_('Chat'),
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Sender'),
    )

    content = models.TextField(verbose_name=_('Content'))
    is_viewed = models.BooleanField(default=False, verbose_name=_('Viewed'))
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at'),
    )

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ['created_at', 'id']
