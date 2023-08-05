from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .choices import MessageType
from .models import Conversation, Message
from .serializers import MessageFullReadSerializer, TextMessageSerializer


class MessengerConsumer(AsyncJsonWebsocketConsumer):
    """ Messenger Consumer """

    async def connect(self):
        self.user = self.scope['user']
        self.convo_uuid = self.scope['url_route']['kwargs']['convo_uuid']
        self.convo_group_name = f'convo-{self.convo_uuid}'
        self.conversation = await self.get_conversation()

        if self.conversation is not None and await self.check_is_member():
            await self.channel_layer.group_add(
                self.convo_group_name,
                self.channel_name,
            )
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.convo_group_name,
            self.channel_name,
        )

    async def receive_json(self, content):
        if content['action'] == 'new_msg':
            if content['msg_type'] == MessageType.TEXT:
                data = await self.save_message(content['content'])
            else:
                data = content['data']
        elif content['action'] == 'viewed':
            msg_viewed = await self.set_message_viewed(content['msg_uuid'])
            data = {
                'msg_uuid': content['msg_uuid'],
                'msg_viewed': msg_viewed,
            }

        await self.channel_layer.group_send(
            self.convo_group_name,
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
    def get_conversation(self):
        try:
            convo = Conversation.objects.get(uuid=self.convo_uuid)
        except Conversation.DoesNotExist:
            return None
        return convo

    @database_sync_to_async
    def check_is_member(self):
        return self.user in self.conversation.members.all()

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
    def set_message_viewed(self, msg_uuid):
        try:
            msg = Message.objects.get(uuid=msg_uuid)
        except Message.DoesNotExist:
            return None

        if self.user != msg.sender:
            msg.viewed = True
            msg.save(update_fields=['viewed'])

        return msg.viewed
