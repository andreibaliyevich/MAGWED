import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import caches
from .models import Chat, Message
from .serializers import MessageSerializer


class MessengerConsumer(AsyncWebsocketConsumer):
    """ Messenger Consumer """

    async def connect(self):
        self.user = self.scope['user']
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = 'chat_%s' % self.chat_id
        self.chat = await self.get_chat()

        if self.chat and await self.check_is_member():
            await self.channel_layer.group_add(
                self.chat_group_name,
                self.channel_name,
            )
            await self.accept()

            await self.send(text_data=json.dumps({
                'messages': await self.get_messages(),
            }))

    async def disconnect(self, close_code):
        wstokens_cache = caches['wstokens']
        wstokens_cache.delete(self.scope['wstoken'])

        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name,
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json['content']
        msg_id, created_at = await self.save_message(content)

        # Send message to chat group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'msg_id': msg_id,
                'sender': self.user.id,
                'content': content,
                'created_at': created_at,
            }
        )

    # Receive message from chat group
    async def chat_message(self, event):
        msg_id = event['msg_id']
        sender = event['sender']
        content = event['content']
        created_at = event['created_at']

        if self.user.id != sender:
            await self.set_message_viewed(msg_id)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'sender': sender,
            'content': content,
            'created_at': created_at,
        }))

    @database_sync_to_async
    def get_chat(self):
        try:
            return Chat.objects.get(id=self.chat_id)
        except Chat.DoesNotExist:
            return None

    @database_sync_to_async
    def check_is_member(self):
        if self.user in self.chat.members.all():
            return True
        else:
            return False

    @database_sync_to_async
    def get_messages(self):
        return MessageSerializer(self.chat.message_set.all(), many=True).data

    @database_sync_to_async
    def save_message(self, content):
        new_msg = Message.objects.create(
            chat=self.chat,
            sender=self.user,
            content=content,
        )

        self.chat.last_message = new_msg
        self.chat.save(update_fields=['last_message'])

        return (new_msg.id, new_msg.created_at.isoformat())

    @database_sync_to_async
    def set_message_viewed(self, msg_id):
        try:
            msg = Message.objects.get(id=msg_id)
        except Message.DoesNotExist:
            pass
        else:
            msg.is_viewed = True
            msg.save(update_fields=['is_viewed'])
