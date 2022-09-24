from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.cache import caches
from .choices import MessageType
from .models import Conversation, Message
from .serializers import MessageFullReadSerializer, TextMessageSerializer


class MessengerConsumer(AsyncJsonWebsocketConsumer):
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

            await self.send_json({
                'messages': await self.get_messages(),
            })

    async def disconnect(self, close_code):
        wstokens_cache = caches['wstokens']
        wstokens_cache.delete(self.scope['wstoken'])

        await self.channel_layer.group_discard(
            self.convo_group_name,
            self.channel_name,
        )

    async def receive_json(self, content):
        if content['msg_type'] == MessageType.TEXT:
            content = content['content']
            msg_data = await self.save_message(content)
        else:
            msg_data = content['msg_data']

        await self.channel_layer.group_send(
            self.convo_group_name,
            {
                'type': 'conversation_message',
                'msg_data': msg_data,
            }
        )

    async def conversation_message(self, event):
        msg_id = event['msg_data']['id']
        sender_id = event['msg_data']['sender']['id']

        if self.user.id != sender_id:
            await self.set_message_viewed(msg_id)

        await self.send_json(event['msg_data'])

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
        return MessageFullReadSerializer(
            self.conversation.messages.all(),
            many=True,
        ).data

    @database_sync_to_async
    def save_message(self, content):
        serializer = TextMessageSerializer(data={'content': content})
        serializer.is_valid(raise_exception=True)
        msg = Message.objects.create(
            conversation=self.conversation,
            sender=self.user,
            msg_type=MessageType.TEXT,
        )
        serializer.save(message=msg)
        return MessageFullReadSerializer(msg).data

    @database_sync_to_async
    def set_message_viewed(self, msg_id):
        try:
            msg = Message.objects.get(id=msg_id)
        except Message.DoesNotExist:
            pass
        else:
            msg.is_viewed = True
            msg.save(update_fields=['is_viewed'])
