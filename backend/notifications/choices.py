from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class ReasonOfNotification(IntegerChoices):
    FOLLOW = 1, _('New follow')
    ARTICLE = 2, _('New article')
    ALBUM = 3, _('New album')
    PHOTO = 4, _('New photo')
    LIKE_ALBUM = 5, _('Like of album')
    LIKE_PHOTO = 6, _('Like of photo')
    COMMENT_ARTICLE = 7, _('Comment of article')
    COMMENT_ALBUM = 8, _('Comment of album')
    COMMENT_PHOTO = 9, _('Comment of photo')
    COMMENT = 10, _('New comment')
    REVIEW = 11, _('New review')
