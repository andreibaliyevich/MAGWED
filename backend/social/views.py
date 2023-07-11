from rest_framework import generics, status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from accounts.permissions import UserIsOrganizer
from accounts.serializers import UserUUIDSerializer
from blog.models import Article
from portfolio.models import Album, Photo
from .filters import FollowFilter, FavoriteFilter, ReviewFilter
from .models import SocialLink, Follow, Favorite, Review, Comment
from .pagination import FollowPagination, FavoritePagination, ReviewPagination
from .permissions import UserIsAuthor
from .serializers import (
    SocialLinkSerializer,
    FollowersSerializer,
    FollowingSerializer,
    FavoriteContentObjectSerializer,
    FavoriteListSerializer,
    ReviewListCreateSerializer,
    ReviewRUDSerializer,
    CommentListCreateSerializer,
    CommentRUDSerializer,
)


UserModel = get_user_model()


class SocialLinkListCreateView(generics.ListCreateAPIView):
    """ Social Link List Create View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    serializer_class = SocialLinkSerializer

    def get_queryset(self):
        return SocialLink.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SocialLinkRUDView(generics.RetrieveUpdateDestroyAPIView):
    """ Social Link Retrieve Update Destroy View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    lookup_field = 'uuid'
    serializer_class = SocialLinkSerializer

    def get_queryset(self):
        return SocialLink.objects.filter(user=self.request.user)


class FollowCreateDestroyView(APIView):
    """ Follow Create Destroy View """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = UserUUIDSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        try:
            Follow.objects.create(follower=request.user, user=user)
        except:
            return Response(
                {'detail': _('You have already follow this user.')},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        serializer = UserUUIDSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        try:
            Follow.objects.get(follower=request.user, user=user).delete()
        except:
            return Response(
                {'detail': _('You do not follow this user.')},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowListView(generics.ListAPIView):
    """ Follow List View """
    permission_classes = [IsAuthenticated]
    queryset = Follow.objects.all()
    pagination_class = FollowPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = FollowFilter

    def get_serializer_class(self):
        if self.request.GET.get('follower', None):
            return FollowingSerializer
        return FollowersSerializer


class FavoriteCreateDestroyView(APIView):
    """ Favorite Create Destroy View """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = FavoriteContentObjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        content_object = serializer.content_object

        try:
            Favorite.objects.create(
                user=request.user,
                content_object=content_object,
            )
        except:
            return Response(
                {'detail': _('You already have this favorite.')},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        serializer = FavoriteContentObjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        content_object = serializer.content_object

        try:
            Favorite.objects.get(
                user=request.user,
                content_type=ContentType.objects.get_for_model(content_object),
                object_uuid=content_object.uuid,
            ).delete()
        except:
            return Response(
                {'detail': _('You do not have this favorite.')},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteListView(generics.ListAPIView):
    """ Favorite List View """
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteListSerializer
    pagination_class = FavoritePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = FavoriteFilter

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class ReviewListCreateView(generics.ListCreateAPIView):
    """ Review List Create View """
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Review.objects.all()
    serializer_class = ReviewListCreateSerializer
    pagination_class = ReviewPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ReviewRUDView(generics.RetrieveUpdateDestroyAPIView):
    """ Review Retrieve Update Destroy View """
    permission_classes = [IsAuthenticated, UserIsAuthor]
    queryset = Review.objects.all()
    lookup_field = 'uuid'
    serializer_class = ReviewRUDSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    """ Comment List Create View """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentListCreateSerializer

    def validate_url(self, **kwargs):
        content_type = kwargs.get('content_type')
        object_uuid = kwargs.get('object_uuid')

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
            self.content_object = object_class.objects.get(uuid=object_uuid)
        except object_class.DoesNotExist:
            return False

        return True

    def get(self, request, *args, **kwargs):
        if not self.validate_url(**kwargs):
            return Response(
                {'detail': _('Not found.')},
                status=status.HTTP_404_NOT_FOUND,
            )
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.validate_url(**kwargs):
            return Response(
                {'detail': _('Not found.')},
                status=status.HTTP_404_NOT_FOUND,
            )
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        return self.content_object.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            content_object=self.content_object,
            author=self.request.user,
        )


class CommentRUDView(generics.RetrieveUpdateDestroyAPIView):
    """ Comment Retrieve Update Destroy View """
    permission_classes = [IsAuthenticated, UserIsAuthor]
    queryset = Comment.objects.all()
    lookup_field = 'uuid'
    serializer_class = CommentRUDSerializer
