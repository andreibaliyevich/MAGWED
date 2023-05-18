from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class CountryChoices(TextChoices):
    BELARUS = 'BY', _('Belarus')
    RUSSIA = 'RU', _('Russia')
    UKRAINE = 'UA', _('Ukraine')


class CityChoices(TextChoices):    
    BREST = 'Brest-BY', _('Brest')
    MINSK = 'Minsk-BY', _('Minsk')

    MOSCOW = 'Moscow-RU', _('Moscow')
    SAINT_PETERSBURG = 'Saint-Petersburg-RU', _('Saint Petersburg')

    KYIV = 'Kyiv-UA', _('Kyiv')
    ODESA = 'Odesa-UA', _('Odesa')


class LanguageChoices(TextChoices):
    Belarusian = 'be', _('Belarusian')
    English = 'en', _('English')
    French = 'fr', _('French')
    German = 'de', _('German')
    Polish = 'pl', _('Polish')
    Portuguese = 'pt', _('Portuguese')
    Russian = 'ru', _('Russian')
    Ukrainian = 'uk', _('Ukrainian')
