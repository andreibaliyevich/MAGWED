from django.contrib import admin
from .models import Notification, Follow, Favorite, Comment, Review


class NotificationAdmin(admin.ModelAdmin):
    """ Notification Model for admin """
    list_display = (
        'id',
        'content_type',
        'object_id',
        'user',
        'viewed',
        'created_at',
    )
    readonly_fields = ('created_at',)


class FollowAdmin(admin.ModelAdmin):
    """ Follow Model for admin """
    list_display = ('id', 'follower', 'user', 'created_at')
    readonly_fields = ('created_at',)


class FavoriteAdmin(admin.ModelAdmin):
    """ Favorite Model for admin """
    list_display = ('id', 'user', 'content_type', 'object_id', 'created_at')
    readonly_fields = ('created_at',)


class CommentAdmin(admin.ModelAdmin):
    """ Comment Model for admin """
    list_display = ('id', 'content_type', 'object_id', 'author', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


class ReviewAdmin(admin.ModelAdmin):
    """ Review Model for admin """
    list_display = ('id', 'organizer', 'author', 'rating', 'created_at')
    readonly_fields = ('created_at', 'updated_at')


admin.site.register(Notification, NotificationAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
