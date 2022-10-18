from django.contrib import admin
from .models import Country, City, Language, Hashtag, Magazine


class CountryAdmin(admin.ModelAdmin):
    """ Country Model for admin """
    list_display = ('name', 'name_local', 'code')
    search_fields = ('code', 'name', 'name_local')


class CityAdmin(admin.ModelAdmin):
    """ City Model for admin """
    list_display = ('name', 'name_local', 'country')
    list_filter = ('country',)
    search_fields = ('name', 'name_local')


class LanguageAdmin(admin.ModelAdmin):
    """ Language Model for admin """
    list_display = ('name', 'name_local', 'code')
    search_fields = ('code', 'name', 'name_local')


class HashtagAdmin(admin.ModelAdmin):
    """ Hashtag Model for admin """
    list_display = ('__str__', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)


class MagazineAdmin(admin.ModelAdmin):
    """ Magazine Model for admin """
    list_display = ('__str__', 'published_at')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('published_at',)


admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(Magazine, MagazineAdmin)
