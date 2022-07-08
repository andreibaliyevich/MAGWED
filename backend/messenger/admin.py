from django.contrib import admin
from .models import Conversation, GroupConversation, Message


class MessageInline(admin.TabularInline):
    """ Message in line for ConversationAdmin """
    model = Message
    extra = 0


class GroupConversationInline(admin.TabularInline):
    """ Group Conversation in line for ConversationAdmin """
    model = GroupConversation
    extra = 0


class ConversationAdmin(admin.ModelAdmin):
    """ Conversation Model for admin """
    list_display = ('id', 'convo_type')
    inlines = (GroupConversationInline, MessageInline)


admin.site.register(Conversation, ConversationAdmin)
