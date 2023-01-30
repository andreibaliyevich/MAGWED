from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .models import Notification
from .serializers import NotificationListSerializer


class NotificationsConsumer(AsyncJsonWebsocketConsumer):
    """ Notifications Consumer """

    async def connect(self):
        self.user = self.scope['user']
        self.notifications_group_name = f'notifications_{self.user.id}'

        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                self.notifications_group_name,
                self.channel_name,
            )
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.notifications_group_name,
            self.channel_name,
        )

    async def receive_json(self, content):
        notice_id = content['notice_id']
        notice_viewed = await self.set_notice_viewed(notice_id)

        await self.send_json({
            'action': 'viewed',
            'notice_id': notice_id,
            'notice_viewed': notice_viewed,
        })

    async def send_notice(self, event):
        await self.send_json({
            'action': event['action'],
            'notice': event['notice'],
        })

    @database_sync_to_async
    def set_notice_viewed(self, notice_id):
        try:
            notice = Notification.objects.get(id=notice_id)
        except Notification.DoesNotExist:
            return False

        notice.viewed = True
        notice.save(update_fields=['viewed'])
        return notice.viewed
