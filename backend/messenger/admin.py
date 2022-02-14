from django.contrib import admin
from .models import Chat, Message


class MessageInline(admin.TabularInline):
    """ Message in line for ChatAdmin """
    model = Message
    extra = 0


class ChatAdmin(admin.ModelAdmin):
    """ Chat Model for admin """
    list_display = ('id',)
    inlines = (MessageInline,)


admin.site.register(Chat, ChatAdmin)
