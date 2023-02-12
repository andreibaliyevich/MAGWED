import uuid
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from main.validators import MinimumImageSizeValidator
from .choices import ConversationType, MessageType
from .utilities import (
    get_conversation_path,
    get_image_message_path,
    get_file_message_path,
)


class Conversation(models.Model):
    """ Conversation Model """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    convo_type = models.PositiveSmallIntegerField(
        choices=ConversationType.choices,
        verbose_name=_('Conversation type'),
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations',
        verbose_name=_('Members'),
    )

    class Meta:
        verbose_name = _('Conversation')
        verbose_name_plural = _('Conversations')
        ordering = ['-uuid']


class GroupConversation(models.Model):
    """ Group Conversation Model """
    conversation = models.OneToOneField(
        Conversation,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='group_details',
        verbose_name=_('Conversation'),
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Owner'),
    )

    name = models.CharField(max_length=150, verbose_name=_('Name'))
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to=get_conversation_path,
        validators=[
            FileExtensionValidator(allowed_extensions=('jpg', 'png')),
            MinimumImageSizeValidator(500, 500),
        ],
        help_text=_(
            'Upload JPG or PNG image. '
            'Required minimum of size %(width)d x %(height)d.'
        ) % {
            'width': 500,
            'height': 500,
        },
        verbose_name=_('Image'),
    )

    class Meta:
        verbose_name = _('Group Conversation')
        verbose_name_plural = _('Group Conversations')
        ordering = ['conversation']


class Message(models.Model):
    """ Message Model """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_('Conversation'),
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Sender'),
    )

    msg_type = models.PositiveSmallIntegerField(
        choices=MessageType.choices,
        verbose_name=_('Message type'),
    )

    created_at = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        verbose_name=_('Created at'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at'),
    )

    viewed = models.BooleanField(default=False, verbose_name=_('Viewed'))

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ['-created_at']


class TextMessage(models.Model):
    """ Text Message Model """
    message = models.OneToOneField(
        Message,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='text',
        verbose_name=_('Message'),
    )
    content = models.TextField(verbose_name=_('Text content'))

    class Meta:
        verbose_name = _('Text Message')
        verbose_name_plural = _('Text Messages')
        ordering = ['message']


class ImageMessage(models.Model):
    """ Image Message Model """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('Message'),
    )
    content = models.ImageField(
        upload_to=get_image_message_path,
        verbose_name=_('Image content'),
    )

    class Meta:
        verbose_name = _('Image Message')
        verbose_name_plural = _('Image Messages')
        ordering = ['message']


class FileMessage(models.Model):
    """ File Message Model """
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='files',
        verbose_name=_('Message'),
    )
    content = models.FileField(
        upload_to=get_file_message_path,
        verbose_name=_('File content'),
    )

    class Meta:
        verbose_name = _('File Message')
        verbose_name_plural = _('File Messages')
        ordering = ['message']
