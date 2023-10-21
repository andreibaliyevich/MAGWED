from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .models import Chat, Message


class ChatListConsumer(AsyncJsonWebsocketConsumer):
    """ Chat List Consumer """

    async def connect(self):
        self.user = self.scope['user']
        self.chat_list_group_name = f'chat-list-{self.user.uuid}'

        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                self.chat_list_group_name,
                self.channel_name,
            )
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_list_group_name,
            self.channel_name,
        )

    async def send_json_data(self, event):
        await self.send_json({
            'action': event['action'],
            'data': event['data'],
        })


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """ Chat Consumer """

    async def connect(self):
        self.user = self.scope['user']
        self.chat_uuid = self.scope['url_route']['kwargs']['chat_uuid']
        self.chat_group_name = f'chat-{self.chat_uuid}'
        self.chat = await self.get_chat()

        if self.chat is not None and await self.check_is_member():
            await self.channel_layer.group_add(
                self.chat_group_name,
                self.channel_name,
            )
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name,
        )

    async def receive_json(self, content):
        if content['action'] == 'viewed':
            msg_viewed = await self.set_message_viewed(content['msg_uuid'])
            data = {
                'msg_uuid': content['msg_uuid'],
                'msg_viewed': msg_viewed,
            }

        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'send_json_data',
                'action': content['action'],
                'data': data,
            }
        )

    async def send_json_data(self, event):
        await self.send_json({
            'action': event['action'],
            'data': event['data'],
        })

    @database_sync_to_async
    def get_chat(self):
        try:
            chat = Chat.objects.get(uuid=self.chat_uuid)
        except Chat.DoesNotExist:
            return None
        return chat

    @database_sync_to_async
    def check_is_member(self):
        return self.user in self.chat.members.all()

    @database_sync_to_async
    def set_message_viewed(self, msg_uuid):
        try:
            msg = Message.objects.get(uuid=msg_uuid)
        except Message.DoesNotExist:
            return None

        if self.user != msg.author:
            msg.viewed = True
            msg.save(update_fields=['viewed'])

        return msg.viewed
