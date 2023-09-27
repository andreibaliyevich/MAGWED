from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'^ws/chat-list/$', consumers.ChatListConsumer.as_asgi()),
    re_path(r'^ws/chat/'
            r'(?P<chat_uuid>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
        consumers.ChatConsumer.as_asgi(),
    ),
]
