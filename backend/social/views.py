from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import IntegrityError
from blog.models import Article
from portfolio.models import Album, Photo
from .models import Notification, Comment
from .serializers import (
    NotificationListSerializer,
    CommentCreateSerializer,
)


class NotificationListView(generics.ListAPIView):
    """ Notification List View """
    queryset = Notification.objects.all()
    serializer_class = NotificationListSerializer


class CommentCreateView(generics.CreateAPIView):
    """ Comment Create View """
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if kwargs['obj_type'] == 'article':
                content_obj = Article.objects.get(id=kwargs['obj_id'])
            elif kwargs['obj_type'] == 'album':
                content_obj = Album.objects.get(id=kwargs['obj_id'])
            elif kwargs['obj_type'] == 'photo':
                content_obj = Photo.objects.get(id=kwargs['obj_id'])
            elif kwargs['obj_type'] == 'comment':
                content_obj = Comment.objects.get(id=kwargs['obj_id'])
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

            try:
                serializer.save(
                    user=request.user,
                    content_object=content_obj,
                )
            except IntegrityError:
                return Response(status=status.HTTP_409_CONFLICT)

            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
