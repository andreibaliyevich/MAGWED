from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'^ws/messenger/'
            r'(?P<convo_uuid>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
        consumers.MessengerConsumer.as_asgi(),
    ),
]
