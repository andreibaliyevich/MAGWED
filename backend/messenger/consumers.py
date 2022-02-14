import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat, Message


class ChatConsumer(AsyncWebsocketConsumer):
    """ Chat Consumer """
    async def connect(self):
        self.user = self.scope['user']
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = 'chat_%s' % self.chat_id

        if await self.check_is_member():
            # Join room group
            await self.channel_layer.group_add(
                self.chat_group_name,
                self.channel_name
            )

            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        msg_content = text_data_json['msg_content']
        msg_id, msg_created_at = await self.save_message(msg_content)

        # Send message to room group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'sender_id': self.user.id,
                'msg_id': msg_id,
                'msg_content': msg_content,
                'msg_created_at': msg_created_at
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        sender_id = event['sender_id']
        msg_id = event['msg_id']
        msg_content = event['msg_content']
        msg_created_at = event['msg_created_at']

        if self.user.id != sender_id:
            await self.set_message_viewed(msg_id)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'sender_id': sender_id,
            'msg_content': msg_content,
            'msg_created_at': msg_created_at
        }))

    @database_sync_to_async
    def check_is_member(self):
        try:
            chat = Chat.objects.get(id=self.chat_id)
        except Chat.DoesNotExist:
            return False
        else:
            if self.user in chat.members.all():
                return True
            else:
                return False

    @database_sync_to_async
    def save_message(self, msg_content):
        try:
            chat = Chat.objects.get(id=self.chat_id)
        except Chat.DoesNotExist:
            return (None, None)
        else:
            new_msg = Message.objects.create(
                chat=chat,
                sender=self.user,
                content=msg_content
            )

            chat.last_message = new_msg
            chat.save(update_fields=['last_message'])

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
