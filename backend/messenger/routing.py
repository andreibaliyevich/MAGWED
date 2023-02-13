from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'^ws/messenger/(?P<convo_uuid>[0-9a-f-]+)/$',
        consumers.MessengerConsumer.as_asgi()),
]
