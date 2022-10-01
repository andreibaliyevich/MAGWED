from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .models import ConnectionHistory


class ConnectionHistoryConsumer(AsyncJsonWebsocketConsumer):
    """ Connection History Consumer """

    async def connect(self):
        self.user = self.scope['user']
        self.device_id = self.scope['url_route']['kwargs']['device_id']
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
            await self.update_user_status(False)
            await self.send_status(False)

    async def send_status(self, status):
        await self.channel_layer.group_send(
            self.ch_group_name,
            {
                'type': 'ch_message',
                'user_id': self.user.id,
                'status': status,
            }
        )

    async def ch_message(self, event):
        await self.send_json({
            'user_id': event['user_id'],
            'status': event['status'],
        })

    @database_sync_to_async
    def update_user_status(self, status):
        ch_obj, created = ConnectionHistory.objects.get_or_create(
            user=self.user,
            device_id=self.device_id,
        )
        ch_obj.online = status
        ch_obj.save(update_fields=['online', 'last_visit'])
