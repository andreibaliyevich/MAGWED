from django.contrib import admin
from .models import Album, Photo


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 0


class AlbumAdmin(admin.ModelAdmin):
    """ Album Model for admin """
    list_display = ('id', 'owner', 'title', 'created_at', 'rating')
    readonly_fields = ('created_at',)
    inlines = (PhotoInline,)


class PhotoAdmin(admin.ModelAdmin):
    """ Photo Model for admin """
    list_display = ('id', 'owner', 'album', 'uploaded_at', 'rating')
    readonly_fields = ('uploaded_at',)


admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
