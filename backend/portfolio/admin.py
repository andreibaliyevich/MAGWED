from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import Album, Photo


class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 0


class AlbumAdmin(admin.ModelAdmin):
    """ Album Model for admin """
    list_display = ('id', 'owner', 'title', 'created_at', 'rating')
    fieldsets = (
        (None, {
            'fields': (
                'owner',
                'title',
            ),
        }),
        (_('Image and Thumbnail'), {
            'fields': ('image', 'thumbnail', 'get_preview'),
        }),
        (_('Description, Hashtags and Date of creation'), {
            'fields': ('description', 'hashtags', 'created_at'),
        }),
        (_('Views, Likes and Rating'), {
            'fields': ('num_views', 'likes', 'rating'),
        }),
    )
    readonly_fields = ('created_at', 'get_preview')
    inlines = (PhotoInline,)

    def get_preview(self, obj):
        return mark_safe(f'<img src="{ obj.thumbnail.url }" height="200">')
    get_preview.short_description = _('Preview')


class PhotoAdmin(admin.ModelAdmin):
    """ Photo Model for admin """
    list_display = (
        'id',
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
        (_('Image and Thumbnail'), {
            'fields': ('image', 'thumbnail', 'get_preview'),
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
        (_('Description, Hashtags and Date of upload'), {
            'fields': ('description', 'hashtags', 'uploaded_at'),
        }),
        (_('Views, Likes and Rating'), {
            'fields': ('num_views', 'likes', 'rating'),
        }),
    )
    readonly_fields = ('uploaded_at', 'get_preview')

    def get_preview(self, obj):
        return mark_safe(f'<img src="{ obj.thumbnail.url }" height="200">')
    get_preview.short_description = _('Preview')


admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
