from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from blog.models import Article
from blog.serializers import ArticleShortReadSerializer
from comments.models import Comment
from portfolio.models import Album, Photo
from reviews.models import Review
from social.models import Follow
from .choices import ReasonOfNotification
from .models import Notification
from .serializers import NotificationShortSerializer


channel_layer = get_channel_layer()


@receiver(post_save, sender=Follow)
def follow_saved(sender, instance, created, **kwargs):
    """ Save and send follow notification """
    notice = Notification.objects.create(
        initiator=instance.follower,
        recipient=instance.user,
        reason=ReasonOfNotification.FOLLOW,
        content_object=instance,
    )

    notice_data = NotificationShortSerializer(notice).data
    if notice_data['initiator']['avatar']:
        avatar_url = notice_data['initiator']['avatar']
        notice_data['initiator']['avatar'] = f'{settings.API_URL}{avatar_url}'
    notice_data['content_object'] = None

    async_to_sync(channel_layer.group_send)(
        f'notification-{notice.recipient.uuid}',
        {
            'type': 'send_json_data',
            'action': 'created',
            'data': notice_data,
        }
    )


@receiver(post_delete, sender=Follow)
def follow_deleted(sender, instance, **kwargs):
    """ Delete and send follow notification """
    notice = Notification.objects.filter(
        initiator=instance.follower,
        recipient=instance.user,
        reason=ReasonOfNotification.FOLLOW,
        content_type=ContentType.objects.get_for_model(Follow),
        object_uuid=instance.uuid,
    ).first()
    if notice is not None:
        notice_uuid = str(notice.uuid)
        notice.delete()
        async_to_sync(channel_layer.group_send)(
            f'notification-{instance.user.uuid}',
            {
                'type': 'send_json_data',
                'action': 'deleted',
                'data': notice_uuid,
            }
        )
