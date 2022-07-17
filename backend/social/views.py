from rest_framework import generics, status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _
from blog.models import Article
from portfolio.models import Album, Photo
from .models import Notification, Comment
from .permissions import UserIsAuthor
from .serializers import (
    NotificationListSerializer,
    CommentListCreateSerializer,
    CommentRUDSerializer,
)


class NotificationListView(generics.ListAPIView):
    """ Notification List View """
    permission_classes = [AllowAny]
    queryset = Notification.objects.all()
    serializer_class = NotificationListSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    """ Comment List Create View """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentListCreateSerializer

    def validate_url(self, **kwargs):
        content_type = kwargs.get('content_type')
        object_id = kwargs.get('object_id')

        if content_type == 'article':
            object_class = Article
        elif content_type == 'album':
            object_class = Album
        elif content_type == 'photo':
            object_class = Photo
        elif content_type == 'comment':
            object_class = Comment
        else:
            return False

        try:
            self.content_object = object_class.objects.get(id=object_id)
        except object_class.DoesNotExist:
            return False

        return True

    def get_queryset(self):
        return self.content_object.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            content_object=self.content_object,
        )

    def get(self, request, *args, **kwargs):
        if not self.validate_url(**kwargs):
            return Response(
                {'detail': _('Not found.')},
                status=status.HTTP_404_NOT_FOUND)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.validate_url(**kwargs):
            return Response(
                {'detail': _('Not found.')},
                status=status.HTTP_404_NOT_FOUND)
        return self.create(request, *args, **kwargs)


class CommentRUDView(generics.RetrieveUpdateDestroyAPIView):
    """ Comment Retrieve Update Destroy View """
    permission_classes = [IsAuthenticated, UserIsAuthor]
    queryset = Comment.objects.all()
    serializer_class = CommentRUDSerializer
