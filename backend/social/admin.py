from django.contrib import admin
from .models import Follow, Favorite, Comment, Review


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """ Follow Model for admin """
    list_display = ('id', 'follower', 'user', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """ Favorite Model for admin """
    list_display = ('id', 'user', 'content_type', 'object_id', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """ Comment Model for admin """
    list_display = ('id', 'content_type', 'object_id', 'author', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """ Review Model for admin """
    list_display = ('id', 'organizer', 'author', 'rating', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
