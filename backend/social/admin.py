from django.contrib import admin
from .models import SocialLink, Follow, Favorite, Comment, Review


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    """ Social Link Model for admin """
    list_display = ('uuid', 'user', 'link_type', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """ Follow Model for admin """
    list_display = ('uuid', 'follower', 'user', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """ Favorite Model for admin """
    list_display = ('uuid', 'user', 'content_type', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """ Comment Model for admin """
    list_display = ('uuid', 'content_type', 'author', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """ Review Model for admin """
    list_display = ('uuid', 'user', 'author', 'rating', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
