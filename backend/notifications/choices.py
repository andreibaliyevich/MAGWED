from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class ActionOfNotification(IntegerChoices):
    FOLLOW = 1, _('New follow')
    ALBUM = 2, _('New album')
    PHOTO = 3, _('New photo')
    LIKE_ALBUM = 4, _('Like of album')
    LIKE_PHOTO = 5, _('Like of photo')
    COMMENT_ARTICLE = 6, _('Comment of article')
    COMMENT_ALBUM = 7, _('Comment of album')
    COMMENT_PHOTO = 8, _('Comment of photo')
    COMMENT = 9, _('New comment')
    REVIEW = 10, _('New review')
