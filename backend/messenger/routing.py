from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'^ws/messenger/(?P<convo_id>\d+)/$',
        consumers.MessengerConsumer.as_asgi()),
]
