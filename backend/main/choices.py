from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class CountryChoices(TextChoices):
    BELARUS = 'BY', _('Belarus')
    RUSSIA = 'RU', _('Russia')
    UKRAINE = 'UA', _('Ukraine')


class CityChoices(TextChoices):
    BREST = 'BY-BR', _('Brest')
    MINSK = 'BY-MI', _('Minsk')
    MOSCOW = 'RU-MO', _('Moscow')
    SAINT_PETERSBURG = 'RU-SP', _('Saint Petersburg')
    KYIV = 'UA-KY', _('Kyiv')
    ODESA = 'UA-OD', _('Odesa')


class LanguageChoices(TextChoices):
    Belarusian = 'be', _('Belarusian')
    English = 'en', _('English')
    French = 'fr', _('French')
    German = 'de', _('German')
    Polish = 'pl', _('Polish')
    Portuguese = 'pt', _('Portuguese')
    Russian = 'ru', _('Russian')
    Ukrainian = 'uk', _('Ukrainian')
