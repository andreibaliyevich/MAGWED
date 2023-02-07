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
