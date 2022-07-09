import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import caches
from .models import Conversation, Message
from .serializers import MessageSerializer


class MessengerConsumer(AsyncWebsocketConsumer):
    """ Messenger Consumer """

    async def connect(self):
        self.user = self.scope['user']
        self.convo_id = self.scope['url_route']['kwargs']['convo_id']
        self.convo_group_name = 'conversation_%s' % self.convo_id
        self.conversation = await self.get_conversation()

        if self.conversation and await self.check_is_member():
            await self.channel_layer.group_add(
                self.convo_group_name,
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
            self.convo_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        content = text_data_json['content']
        msg_id, created_at = await self.save_message(content)

        await self.channel_layer.group_send(
            self.convo_group_name,
            {
                'type': 'conversation_message',
                'msg_id': msg_id,
                'sender': {
                    'id': self.user.id,
                    'name': self.user.name,
                    'avatar': self.user.avatar.url,
                },
                'content': content,
                'created_at': created_at,
            }
        )

    async def conversation_message(self, event):
        print(event)
        msg_id = event['msg_id']
        sender = event['sender']
        content = event['content']
        created_at = event['created_at']

        if self.user.id != sender['id']:
            await self.set_message_viewed(msg_id)

        await self.send(text_data=json.dumps({
            'sender': sender,
            'content': content,
            'created_at': created_at,
        }))

    @database_sync_to_async
    def get_conversation(self):
        try:
            return Conversation.objects.get(id=self.convo_id)
        except Conversation.DoesNotExist:
            return None

    @database_sync_to_async
    def check_is_member(self):
        if self.user in self.conversation.members.all():
            return True
        else:
            return False

    @database_sync_to_async
    def get_messages(self):
        return MessageSerializer(
            self.conversation.messages.all(),
            many=True,
        ).data

    @database_sync_to_async
    def save_message(self, content):
        new_msg = Message.objects.create(
            conversation=self.conversation,
            sender=self.user,
            content=content,
        )
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
