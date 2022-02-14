from django.db import models
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    """ Country Model """
    code = models.SlugField(
        max_length=2,
        primary_key=True,
        verbose_name=_('Code'),
    )
    name = models.CharField(max_length=64, verbose_name=_('Name'))
    name_local = models.CharField(max_length=64, verbose_name=_('Name (local)'))

    def __str__(self):
        return f'{ self.name_local } ({ self.name })'

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        ordering = ['name', 'code']


class City(models.Model):
    """ City Model """
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        verbose_name=_('Country'),
    )

    name = models.CharField(max_length=64, verbose_name=_('Name'))
    name_local = models.CharField(max_length=64, verbose_name=_('Name (local)'))
    slug = models.SlugField(max_length=64, verbose_name=_('Slug'))

    def __str__(self):
        return f'{ self.name_local } ({ self.name })'

    class Meta:
        verbose_name = _('City')
        verbose_name_plural = _('Cities')
        ordering = ['name', 'country']
        unique_together = ['country', 'slug']


class Language(models.Model):
    """ Language Model """
    code = models.SlugField(
        max_length=2,
        primary_key=True,
        verbose_name=_('Code'),
    )
    name = models.CharField(max_length=64, verbose_name=_('Name'))
    name_local = models.CharField(max_length=64, verbose_name=_('Name (local)'))

    def __str__(self):
        return f'{ self.name_local } ({ self.name })'

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')
        ordering = ['name', 'code']
