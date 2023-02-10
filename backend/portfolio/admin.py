from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import Album, Photo


class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 0


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    """ Album Model for admin """
    list_display = ('uuid', 'owner', 'title', 'created_at', 'rating')
    fieldsets = (
        (None, {
            'fields': (
                'owner',
            ),
        }),
        (_('Image'), {
            'fields': ('image', 'get_preview'),
        }),
        (_('Info'), {
            'fields': ('title', 'description', 'hashtags', 'created_at'),
        }),
        (_('Social'), {
            'fields': ('num_views', 'likes', 'rating'),
        }),
    )
    readonly_fields = ('created_at', 'get_preview')
    inlines = (PhotoInline,)

    def get_preview(self, obj):
        return mark_safe(f'<img src="{ obj.thumbnail.url }" height="100">')
    get_preview.short_description = _('Preview')


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ Photo Model for admin """
    list_display = (
        'uuid',
        'owner',
        'album',
        'uploaded_at',
        'rating',
        'get_preview',
    )
    fieldsets = (
        (None, {
            'fields': (
                'owner',
                'album',
            ),
        }),
        (_('Image'), {
            'fields': ('image', 'get_preview'),
        }),
        (_('Photo details'), {
            'fields': (
                'device',
                'f_number',
                'exposure_time',
                'focal_length',
                'photographic_sensitivity',
            ),
        }),
        (_('Info'), {
            'fields': ('title', 'description', 'hashtags', 'uploaded_at'),
        }),
        (_('Social'), {
            'fields': ('num_views', 'likes', 'rating'),
        }),
    )
    readonly_fields = ('uploaded_at', 'get_preview')

    def get_preview(self, obj):
        return mark_safe(f'<img src="{ obj.thumbnail.url }" height="100">')
    get_preview.short_description = _('Preview')
