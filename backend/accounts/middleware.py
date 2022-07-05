from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.cache import caches


UserModel = get_user_model()


@database_sync_to_async
def get_user(wstoken):
    wstokens_cache = caches['wstokens']
    user_id = wstokens_cache.get(wstoken)

    if user_id is None:
        return AnonymousUser()

    try:
        return UserModel.objects.get(id=user_id)
    except UserModel.DoesNotExist:
        return AnonymousUser()


class WebSocketAuthMiddleware:
    """ WebSocket Auth Middleware """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        wstoken = scope['query_string'].decode()
        scope['user'] = await get_user(wstoken)
        scope['wstoken'] = wstoken
        return await self.app(scope, receive, send)
