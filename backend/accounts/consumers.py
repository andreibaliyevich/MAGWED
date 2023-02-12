from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .models import ConnectionHistory


class ConnectionHistoryConsumer(AsyncJsonWebsocketConsumer):
    """ Connection History Consumer """

    async def connect(self):
        self.user = self.scope['user']
        self.device_uuid = self.scope['url_route']['kwargs']['device_uuid']
        self.ch_group_name = 'users'

        await self.channel_layer.group_add(
            self.ch_group_name,
            self.channel_name,
        )
        await self.accept()

        if self.user.is_authenticated:
            await self.update_user_status(True)
            await self.send_status(True)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.ch_group_name,
            self.channel_name,
        )

        if self.user.is_authenticated:
            user_status = await self.update_user_status(False)
            await self.send_status(user_status)

    async def send_status(self, online):
        await self.channel_layer.group_send(
            self.ch_group_name,
            {
                'type': 'ch_message',
                'user_uuid': self.user.uuid,
                'online': online,
            }
        )

    async def ch_message(self, event):
        await self.send_json({
            'user_uuid': event['user_uuid'],
            'online': event['online'],
        })

    @database_sync_to_async
    def update_user_status(self, online):
        ch_obj, created = ConnectionHistory.objects.get_or_create(
            user=self.user,
            device_uuid=self.device_uuid,
        )

        if not (online and created):
            ch_obj.online = online
            ch_obj.save(update_fields=['online', 'last_visit'])

        if not online:
            if self.user.connection_histories.filter(online=True).count() > 0:
                return True
            else:
                return False
