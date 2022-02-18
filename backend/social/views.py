from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import IntegrityError
from blog.models import Article
from portfolio.models import Album, Photo
from .models import Notification, Comment
from .serializers import (
    NotificationListSerializer,
    CommentCreateSerializer,
)


class NotificationListView(APIView):
    """ Notification List View """

    def get(self, request):
        notifications = Notification.objects.all()
        serializer = NotificationListSerializer(notifications, many=True)
        return Response(serializer.data)


class CommentCreateView(APIView):
    """ Comment Create View """

    def post(self, request, obj_type, obj_id):
        comment = CommentCreateSerializer(data=request.data)
        if comment.is_valid():
            if obj_type == 'article':
                comment_obj = Article.objects.get(id=obj_id)
            elif obj_type == 'album':
                comment_obj = Album.objects.get(id=obj_id)
            elif obj_type == 'photo':
                comment_obj = Photo.objects.get(id=obj_id)
            elif obj_type == 'comment':
                comment_obj = Comment.objects.get(id=obj_id)
            else:
                return Response(status=400)

            try:
                new_comment = comment.save(
                    user=request.user,
                    content_object=comment_obj,
                )
            except IntegrityError:
                return Response(status=405)
        return Response(status=201)
