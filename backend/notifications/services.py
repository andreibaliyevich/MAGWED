from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from .serializers import NotificationListSerializer


channel_layer = get_channel_layer()


def send_notification(notice, action):
    """ Send notification to Consumer """
    notice_data = NotificationListSerializer(notice).data

    if notice_data['initiator']['avatar']:
        url = notice_data['initiator']['avatar']
        notice_data['initiator']['avatar'] = f'{settings.API_URL}{url}'

    if notice_data['content_object']['thumbnail']:
        url = notice_data['content_object']['thumbnail']
        notice_data['content_object']['thumbnail'] = f'{settings.API_URL}{url}'

    async_to_sync(channel_layer.group_send)(
        f'notifications_{notice.recipient.id}',
        {
            'type': 'send_notice',
            'action': action,
            'notice': notice_data,
        }
    )
