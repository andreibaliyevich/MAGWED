from django.contrib import admin
from .models import SocialLink


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    """ Social Link Model for admin """
    list_display = ('id', 'user', 'link_type')
