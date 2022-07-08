from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class ConversationType(IntegerChoices):
    DIALOG = 1, _('Dialog')
    GROUP = 2, _('Group')
