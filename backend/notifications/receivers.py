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
from portfolio.serializers import (
    AlbumShortReadSerializer,
    PhotoShortReadSerializer,
)
from portfolio.signals import like_obj, dislike_obj
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


@receiver(post_save, sender=Article)
def article_saved(sender, instance, created, **kwargs):
    """ Save and send article notification """
    if created:
        for follow in instance.author.followers.all():
            notice = Notification.objects.create(
                initiator=instance.author,
                recipient=follow.follower,
                reason=ReasonOfNotification.ARTICLE,
                content_object=instance,
            )

            notice_data = NotificationShortSerializer(notice).data
            if notice_data['initiator']['avatar']:
                avatar_url = notice_data['initiator']['avatar']
                notice_data['initiator']['avatar'] = f'{settings.API_URL}{avatar_url}'

            notice_data['content_object'] = ArticleShortReadSerializer(instance).data
            thumbnail_url = notice_data['content_object']['thumbnail']
            notice_data['content_object']['thumbnail'] = f'{settings.API_URL}{thumbnail_url}'

            async_to_sync(channel_layer.group_send)(
                f'notification-{notice.recipient.uuid}',
                {
                    'type': 'send_json_data',
                    'action': 'created',
                    'data': notice_data,
                }
            )
    else:
        content_object_data = ArticleShortReadSerializer(instance).data
        thumbnail_url = content_object_data['thumbnail']
        content_object_data['thumbnail'] = f'{settings.API_URL}{thumbnail_url}'

        notices_values = Notification.objects.filter(
            initiator=instance.author,
            reason=ReasonOfNotification.ARTICLE,
            content_type=ContentType.objects.get_for_model(Article),
            object_uuid=instance.uuid,
        ).values('uuid', 'recipient__uuid')

        for value in notices_values:
            async_to_sync(channel_layer.group_send)(
                f"notification-{value['recipient__uuid']}",
                {
                    'type': 'send_json_data',
                    'action': 'updated',
                    'data': {
                        'uuid': str(value['uuid']),
                        'content_object': content_object_data,
                    },
                }
            )


@receiver(post_delete, sender=Article)
def article_deleted(sender, instance, **kwargs):
    """ Delete and send article notification """
    notices = Notification.objects.filter(
        initiator=instance.author,
        reason=ReasonOfNotification.ARTICLE,
        content_type=ContentType.objects.get_for_model(Article),
        object_uuid=instance.uuid,
    )
    values_list = list(notices.values('uuid', 'recipient__uuid'))
    notices.delete()
    for value in values_list:
        async_to_sync(channel_layer.group_send)(
            f"notification-{value['recipient__uuid']}",
            {
                'type': 'send_json_data',
                'action': 'deleted',
                'data': str(value['uuid']),
            }
        )


@receiver(post_save, sender=Album)
def album_saved(sender, instance, created, **kwargs):
    """ Save and send album notification """
    if created:
        for follow in instance.owner.followers.all():
            notice = Notification.objects.create(
                initiator=instance.owner,
                recipient=follow.follower,
                reason=ReasonOfNotification.ALBUM,
                content_object=instance,
            )

            notice_data = NotificationShortSerializer(notice).data
            if notice_data['initiator']['avatar']:
                avatar_url = notice_data['initiator']['avatar']
                notice_data['initiator']['avatar'] = f'{settings.API_URL}{avatar_url}'

            notice_data['content_object'] = AlbumShortReadSerializer(instance).data
            thumbnail_url = notice_data['content_object']['thumbnail']
            notice_data['content_object']['thumbnail'] = f'{settings.API_URL}{thumbnail_url}'

            async_to_sync(channel_layer.group_send)(
                f'notification-{notice.recipient.uuid}',
                {
                    'type': 'send_json_data',
                    'action': 'created',
                    'data': notice_data,
                }
            )
    else:
        content_object_data = AlbumShortReadSerializer(instance).data
        thumbnail_url = content_object_data['thumbnail']
        content_object_data['thumbnail'] = f'{settings.API_URL}{thumbnail_url}'

        notices_values = Notification.objects.filter(
            initiator=instance.owner,
            reason=ReasonOfNotification.ALBUM,
            content_type=ContentType.objects.get_for_model(Album),
            object_uuid=instance.uuid,
        ).values('uuid', 'recipient__uuid')

        for value in notices_values:
            async_to_sync(channel_layer.group_send)(
                f"notification-{value['recipient__uuid']}",
                {
                    'type': 'send_json_data',
                    'action': 'updated',
                    'data': {
                        'uuid': str(value['uuid']),
                        'content_object': content_object_data,
                    },
                }
            )


@receiver(post_delete, sender=Album)
def album_deleted(sender, instance, **kwargs):
    """ Delete and send album notification """
    notices = Notification.objects.filter(
        initiator=instance.owner,
        reason=ReasonOfNotification.ALBUM,
        content_type=ContentType.objects.get_for_model(Album),
        object_uuid=instance.uuid,
    )
    values_list = list(notices.values('uuid', 'recipient__uuid'))
    notices.delete()
    for value in values_list:
        async_to_sync(channel_layer.group_send)(
            f"notification-{value['recipient__uuid']}",
            {
                'type': 'send_json_data',
                'action': 'deleted',
                'data': str(value['uuid']),
            }
        )


@receiver(post_save, sender=Photo)
def photo_saved(sender, instance, created, **kwargs):
    """ Save and send photo notification """
    if instance.album is None:
        if created:
            for follow in instance.owner.followers.all():
                notice = Notification.objects.create(
                    initiator=instance.owner,
                    recipient=follow.follower,
                    reason=ReasonOfNotification.PHOTO,
                    content_object=instance,
                )

                notice_data = NotificationShortSerializer(notice).data
                if notice_data['initiator']['avatar']:
                    avatar_url = notice_data['initiator']['avatar']
                    notice_data['initiator']['avatar'] = f'{settings.API_URL}{avatar_url}'

                notice_data['content_object'] = PhotoShortReadSerializer(instance).data
                thumbnail_url = notice_data['content_object']['thumbnail']
                notice_data['content_object']['thumbnail'] = f'{settings.API_URL}{thumbnail_url}'

                async_to_sync(channel_layer.group_send)(
                    f'notification-{notice.recipient.uuid}',
                    {
                        'type': 'send_json_data',
                        'action': 'created',
                        'data': notice_data,
                    }
                )
        else:
            content_object_data = PhotoShortReadSerializer(instance).data
            thumbnail_url = content_object_data['thumbnail']
            content_object_data['thumbnail'] = f'{settings.API_URL}{thumbnail_url}'

            notices_values = Notification.objects.filter(
                initiator=instance.owner,
                reason=ReasonOfNotification.PHOTO,
                content_type=ContentType.objects.get_for_model(Photo),
                object_uuid=instance.uuid,
            ).values('uuid', 'recipient__uuid')

            for value in notices_values:
                async_to_sync(channel_layer.group_send)(
                    f"notification-{value['recipient__uuid']}",
                    {
                        'type': 'send_json_data',
                        'action': 'updated',
                        'data': {
                            'uuid': str(value['uuid']),
                            'content_object': content_object_data,
                        },
                    }
                )


@receiver(post_delete, sender=Photo)
def photo_deleted(sender, instance, **kwargs):
    """ Delete and send photo notification """
    if instance.album is None:
        notices = Notification.objects.filter(
            initiator=instance.owner,
            reason=ReasonOfNotification.PHOTO,
            content_type=ContentType.objects.get_for_model(Photo),
            object_uuid=instance.uuid,
        )
        values_list = list(notices.values('uuid', 'recipient__uuid'))
        notices.delete()
        for value in values_list:
            async_to_sync(channel_layer.group_send)(
                f"notification-{value['recipient__uuid']}",
                {
                    'type': 'send_json_data',
                    'action': 'deleted',
                    'data': str(value['uuid']),
                }
            )


@receiver(like_obj, sender=Album)
def album_liked(sender, instance, user, **kwargs):
    """ Save and send album liked notification """
    if instance.owner.uuid != user.uuid:
        notice = Notification.objects.create(
            initiator=user,
            recipient=instance.owner,
            reason=ReasonOfNotification.LIKE_ALBUM,
            content_object=instance,
        )

        notice_data = NotificationShortSerializer(notice).data
        if notice_data['initiator']['avatar']:
            avatar_url = notice_data['initiator']['avatar']
            notice_data['initiator']['avatar'] = f'{settings.API_URL}{avatar_url}'

        notice_data['content_object'] = AlbumShortReadSerializer(instance).data
        thumbnail_url = notice_data['content_object']['thumbnail']
        notice_data['content_object']['thumbnail'] = f'{settings.API_URL}{thumbnail_url}'

        async_to_sync(channel_layer.group_send)(
            f'notification-{notice.recipient.uuid}',
            {
                'type': 'send_json_data',
                'action': 'created',
                'data': notice_data,
            }
        )


@receiver(dislike_obj, sender=Album)
def album_disliked(sender, instance, user, **kwargs):
    """ Delete and send album disliked notification """
    if instance.owner.uuid != user.uuid:
        notice = Notification.objects.filter(
            initiator=user,
            recipient=instance.owner,
            reason=ReasonOfNotification.LIKE_ALBUM,
            content_type=ContentType.objects.get_for_model(Album),
            object_uuid=instance.uuid,
        ).first()
        if notice is not None:
            notice_uuid = str(notice.uuid)
            notice.delete()
            async_to_sync(channel_layer.group_send)(
                f'notification-{instance.owner.uuid}',
                {
                    'type': 'send_json_data',
                    'action': 'deleted',
                    'data': notice_uuid,
                }
            )


@receiver(like_obj, sender=Photo)
def photo_liked(sender, instance, user, **kwargs):
    """ Save and send album liked notification """
    if instance.owner.uuid != user.uuid:
        notice = Notification.objects.create(
            initiator=user,
            recipient=instance.owner,
            reason=ReasonOfNotification.LIKE_PHOTO,
            content_object=instance,
        )

        notice_data = NotificationShortSerializer(notice).data
        if notice_data['initiator']['avatar']:
            avatar_url = notice_data['initiator']['avatar']
            notice_data['initiator']['avatar'] = f'{settings.API_URL}{avatar_url}'
        
        notice_data['content_object'] = PhotoShortReadSerializer(instance).data
        thumbnail_url = notice_data['content_object']['thumbnail']
        notice_data['content_object']['thumbnail'] = f'{settings.API_URL}{thumbnail_url}'

        async_to_sync(channel_layer.group_send)(
            f'notification-{notice.recipient.uuid}',
            {
                'type': 'send_json_data',
                'action': 'created',
                'data': notice_data,
            }
        )


@receiver(dislike_obj, sender=Photo)
def photo_disliked(sender, instance, user, **kwargs):
    """ Delete and send album disliked notification """
    if instance.owner.uuid != user.uuid:
        notice = Notification.objects.filter(
            initiator=user,
            recipient=instance.owner,
            reason=ReasonOfNotification.LIKE_PHOTO,
            content_type=ContentType.objects.get_for_model(Photo),
            object_uuid=instance.uuid,
        ).first()
        if notice is not None:
            notice_uuid = str(notice.uuid)
            notice.delete()
            async_to_sync(channel_layer.group_send)(
                f'notification-{instance.owner.uuid}',
                {
                    'type': 'send_json_data',
                    'action': 'deleted',
                    'data': notice_uuid,
                }
            )
