from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class LinkType(IntegerChoices):
    FACEBOOK = 1, _('Facebook')
    TWITTER = 2, _('Twitter')
    INSTAGRAM = 3, _('Instagram')
    LINKEDIN = 4, _('LinkedIn')
    SPOTIFY = 5, _('Spotify')
    YOUTUBE = 6, _('YouTube')
    SOUNDCLOUD = 7, _('SoundCloud')
    PINTEREST = 8, _('Pinterest')
    VK = 9, _('VK')


class RatingOfReview(IntegerChoices):
    FIVE = 5, _('5 stars')
    FOUR = 4, _('4 stars')
    THREE = 3, _('3 stars')
    TWO = 2, _('2 stars')
    ONE = 1, _('1 star')

    __empty__ = _('Choose rating')
