from django.contrib import admin
from .models import Country, City, Language, Magazine


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """ Country Model for admin """
    list_display = ('name', 'name_local', 'code')
    search_fields = ('code', 'name', 'name_local')


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """ City Model for admin """
    list_display = ('name', 'name_local', 'country')
    list_filter = ('country',)
    search_fields = ('name', 'name_local')


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    """ Language Model for admin """
    list_display = ('name', 'name_local', 'code')
    search_fields = ('code', 'name', 'name_local')


@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    """ Magazine Model for admin """
    list_display = ('__str__', 'published_at')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('published_at',)
