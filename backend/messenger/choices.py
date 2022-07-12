from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class ConversationType(IntegerChoices):
    DIALOG = 1, _('Dialog')
    GROUP = 2, _('Group')


class MessageType(IntegerChoices):
    TEXT = 1, _('Text')
    IMAGE = 2, _('Image')
    FILE = 3, _('File')
