from django.contrib import admin
from .models import Tag, TaggedItem


class TaggedItemInline(admin.TabularInline):
    model = TaggedItem
    extra = 0


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """ Tag Model for admin """
    list_display = ('__str__', 'created_at')
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at',)
    inlines = (TaggedItemInline,)
