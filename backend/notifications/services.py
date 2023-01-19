from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .serializers import NotificationListSerializer


channel_layer = get_channel_layer()


def send_notification(notice, action):
    """ Send notification to Consumer """
    notifications_group_name = 'notifications_%s' % notice.recipient.id

    notice_data = NotificationListSerializer(notice).data
    notice_data.update({'action': action})

    async_to_sync(channel_layer.group_send)(
        notifications_group_name,
        {
            'type': 'send_notice',
            'notice_data': notice_data,
        }
    )
