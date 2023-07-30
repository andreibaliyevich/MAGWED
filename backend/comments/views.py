from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from django.contrib.contenttypes.models import ContentType
from .filters import CommentFilter
from .models import Comment
from .pagination import CommentPagination
from .permissions import UserIsAuthor
from .serializers import CommentListCreateSerializer, CommentRUDSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    """ Comment List Create View """
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentListCreateSerializer
    pagination_class = CommentPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = CommentFilter


class CommentRUDView(generics.RetrieveUpdateDestroyAPIView):
    """ Comment Retrieve Update Destroy View """
    permission_classes = [IsAuthenticated, UserIsAuthor]
    queryset = Comment.objects.all()
    lookup_field = 'uuid'
    serializer_class = CommentRUDSerializer
