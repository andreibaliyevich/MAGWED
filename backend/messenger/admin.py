from django.contrib import admin
from .models import (
    Conversation,
    GroupConversation,
    Message,
    TextMessage,
    ImageMessage,
    FileMessage,
)


class GroupConversationInline(admin.TabularInline):
    """ Group Conversation in line for ConversationAdmin """
    model = GroupConversation
    extra = 0


class ConversationAdmin(admin.ModelAdmin):
    """ Conversation Model for admin """
    list_display = ('id', 'convo_type')
    inlines = (GroupConversationInline,)


class TextMessageInline(admin.TabularInline):
    """ TextMessage in line for ConversationAdmin """
    model = TextMessage
    extra = 0


class ImageMessageInline(admin.TabularInline):
    """ ImageMessage in line for ConversationAdmin """
    model = ImageMessage
    extra = 0


class FileMessageInline(admin.TabularInline):
    """ FileMessage in line for ConversationAdmin """
    model = FileMessage
    extra = 0


class MessageAdmin(admin.ModelAdmin):
    """ Message Model for admin """
    list_display = ('id', 'conversation', 'sender', 'msg_type', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    inlines = (TextMessageInline, ImageMessageInline, FileMessageInline)


admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, MessageAdmin)
