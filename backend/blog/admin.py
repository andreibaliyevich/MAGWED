from tinymce.widgets import TinyMCE
from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import (
    Category,
    CategoryTranslation,
    Article,
    ArticleTranslation,
    ArticleImage,
)


class CategoryTranslationInline(admin.StackedInline):
    model = CategoryTranslation
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Category Model for admin """
    list_display = ('__str__',)
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('name', 'slug'),
        }),
        (_('Metadata'), {
            'fields': ('meta_description', 'meta_keywords'),
        }),
    )
    inlines = (CategoryTranslationInline,)


class ArticleTranslationInline(admin.StackedInline):
    model = ArticleTranslation
    extra = 0
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """ Article Model for admin """
    list_display = ('__str__', 'author', 'published_at')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': (
                'author',
                'categories',
                'title',
                'slug',
            ),
        }),
        (_('Metadata'), {
            'fields': ('meta_description', 'meta_keywords'),
        }),
        (_('Image'), {
            'fields': ('image', 'get_preview'),
        }),
        (_('Content and Hashtags'), {
            'fields': ('content', 'hashtags'),
        }),
        (_('Published and Views'), {
            'fields': ('published_at', 'num_views'),
        }),
    )
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
    readonly_fields = ('published_at', 'num_views', 'get_preview')
    inlines = (ArticleTranslationInline,)

    def get_preview(self, obj):
        return mark_safe(f'<img src="{ obj.thumbnail.url }" height="100">')
    get_preview.short_description = _('Preview')


@admin.register(ArticleImage)
class ArticleImageAdmin(admin.ModelAdmin):
    """ Article Image Model for admin """
    list_display = ('id', 'file', 'get_preview')
    readonly_fields = ('get_preview',)

    def get_preview(self, obj):
        return mark_safe(f'<img src="{ obj.file.url }" height="100">')
    get_preview.short_description = _('Preview')
