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
            await self.set_user_online()
            await self.send_status(True)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.ch_group_name,
            self.channel_name,
        )

        if self.user.is_authenticated:
            online = await self.set_user_offline()
            await self.send_status(online)

    async def receive_json(self, content):
        await self.send_status(content['online'])

    async def send_status(self, online):
        await self.channel_layer.group_send(
            self.ch_group_name,
            {
                'type': 'send_json_data',
                'user_uuid': str(self.user.uuid),
                'online': online,
            }
        )

    async def send_json_data(self, event):
        await self.send_json({
            'user_uuid': event['user_uuid'],
            'online': event['online'],
        })

    @database_sync_to_async
    def set_user_online(self):
        ch_obj, created = ConnectionHistory.objects.get_or_create(
            user=self.user,
            device_uuid=self.device_uuid,
        )

        if not created:
            ch_obj.online = True
            ch_obj.save(update_fields=['online', 'last_visit'])

    @database_sync_to_async
    def set_user_offline(self):
        ch_obj, created = ConnectionHistory.objects.get_or_create(
            user=self.user,
            device_uuid=self.device_uuid,
        )

        ch_obj.online = False
        ch_obj.save(update_fields=['online', 'last_visit'])

        return bool(self.user.connection_histories.filter(online=True).count())
