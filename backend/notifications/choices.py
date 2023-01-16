from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class NotificationType(IntegerChoices):
    NEW_FOLLOW = 1, _('New follow')
    NEW_ALBUM = 2, _('New album')
    NEW_PHOTO = 3, _('New photo')
    NEW_REVIEW = 4, _('New review')
    NEW_COMMENT = 5, _('New comment')
