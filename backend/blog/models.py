from easy_thumbnails.fields import ThumbnailerImageField
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from main.model_fields import TranslatedField
from main.models import Hashtag
from main.utilities import get_thumbnail_path
from .utilities import get_article_path


class Category(models.Model):
    """ Category Model """
    name = models.CharField(max_length=64, verbose_name=_('Name'))
    translated_name = TranslatedField('name')
    slug = models.SlugField(max_length=64, unique=True, verbose_name=_('Slug'))

    meta_description = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('Description'),
    )
    meta_keywords = models.CharField(
        blank=True,
        max_length=255,
        help_text=_('Separate keywords with commas.'),
        verbose_name=_('Keywords'),
    )
    translated_meta_description = TranslatedField('meta_description')
    translated_meta_keywords = TranslatedField('meta_keywords')

    def __str__(self):
        return self.translated_name

    def get_absolute_url(self):
        return reverse('blog:articles_by_category', args=[self.slug])

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name', 'id']


class CategoryTranslation(models.Model):
    """ Category Translation Model """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name=_('Category'),
    )
    language = models.CharField(
        max_length=2,
        choices=settings.LANGUAGES[1:],
        verbose_name=_('Language'),
    )

    name = models.CharField(max_length=64, verbose_name=_('Name'))

    meta_description = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('Description'),
    )
    meta_keywords = models.CharField(
        blank=True,
        max_length=255,
        help_text=_('Separate keywords with commas.'),
        verbose_name=_('Keywords'),
    )

    class Meta:
        verbose_name = _('Category Translation')
        verbose_name_plural = _('Category Translations')
        ordering = ['category', 'language']
        unique_together = ['category', 'language']


class Article(models.Model):
    """ Article Model """
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Author'),
    )
    categories = models.ManyToManyField(Category, verbose_name=_('Categories'))

    title = models.CharField(max_length=128, verbose_name=_('Title'))
    translated_title = TranslatedField('title')
    slug = models.SlugField(max_length=128, unique=True, verbose_name=_('Slug'))

    meta_description = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('Description'),
    )
    meta_keywords = models.CharField(
        blank=True,
        max_length=255,
        help_text=_('Separate keywords with commas.'),
        verbose_name=_('Keywords'),
    )
    translated_meta_description = TranslatedField('meta_description')
    translated_meta_keywords = TranslatedField('meta_keywords')

    image = models.ImageField(
        upload_to=get_article_path,
        verbose_name=_('Image'),
    )
    thumbnail = ThumbnailerImageField(
        upload_to=get_thumbnail_path,
        resize_source={
            'size': (800, 600),
            'crop': 'smart',
            'autocrop': True,
            'quality': 100,
        },
        verbose_name=_('Thumbnail'),
    )

    content = models.TextField(verbose_name=_('Content'))
    translated_content = TranslatedField('content')
    
    hashtags = models.ManyToManyField(
        Hashtag,
        blank=True,
        verbose_name=_('Tags'),
    )

    published_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Published at'),
    )

    num_views = models.IntegerField(
        default=0,
        verbose_name=_('Number of views'),
    )

    def __str__(self):
        return self.translated_title

    def get_absolute_url(self):
        return reverse('blog:article_detail', args=[self.id, self.slug])

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        ordering = ['-published_at', '-id']


class ArticleTranslation(models.Model):
    """ Article Translation Model """
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name=_('Article'),
    )
    language = models.CharField(
        max_length=2,
        choices=settings.LANGUAGES[1:],
        verbose_name=_('Language'),
    )

    title = models.CharField(max_length=128, verbose_name=_('Title'))

    meta_description = models.CharField(
        blank=True,
        max_length=255,
        verbose_name=_('Description'),
    )
    meta_keywords = models.CharField(
        blank=True,
        max_length=255,
        help_text=_('Separate keywords with commas.'),
        verbose_name=_('Keywords'),
    )

    content = models.TextField(verbose_name=_('Content'))

    class Meta:
        verbose_name = _('Article Translation')
        verbose_name_plural = _('Article Translations')
        ordering = ['article', 'language']
        unique_together = ['article', 'language']


class ArticleImage(models.Model):
    """ Article Image Model """
    file = models.ImageField(upload_to=get_article_path, verbose_name=_('File'))

    class Meta:
        verbose_name = _('Image of Article')
        verbose_name_plural = _('Images of Articles')
        ordering = ['-id']