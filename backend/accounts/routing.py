from django.urls import re_path
from . import consumers


websocket_urlpatterns = [
    re_path(r'^ws/connection/(?P<device_id>[0-9a-f-]+)/$',
        consumers.ConnectionHistoryConsumer.as_asgi()),
]
