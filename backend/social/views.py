from rest_framework import generics, status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import ugettext_lazy as _
from accounts.models import Organizer
from accounts.permissions import UserIsOrganizer
from blog.models import Article
from portfolio.models import Album, Photo
from .models import SocialLink, Follow, Comment, Review
from .permissions import UserIsAuthor
from .serializers import (
    SocialLinkSerializer,
    FollowSerializer,
    CommentListCreateSerializer,
    CommentRUDSerializer,
    ReviewListCreateSerializer,
    ReviewRUDSerializer,
)


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


class FollowView(APIView):
    """ Follow View """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = FollowSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        try:
            Follow.objects.create(follower=request.user, user=user)
        except:
            return Response(
                {'detail': _('You have already follow.')},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, *args, **kwargs):
        serializer = FollowSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        try:
            Follow.objects.get(follower=request.user, user=user).delete()
        except:
            return Response(
                {'detail': _('You have already unfollow.')},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


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
                status=status.HTTP_404_NOT_FOUND)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.validate_url(**kwargs):
            return Response(
                {'detail': _('Not found.')},
                status=status.HTTP_404_NOT_FOUND)
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
    lookup_field = 'uuid'
    queryset = Comment.objects.all()
    serializer_class = CommentRUDSerializer


class ReviewListCreateView(generics.ListCreateAPIView):
    """ Review List Create View """
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ReviewListCreateSerializer

    def validate_url(self, **kwargs):
        profile_url = kwargs.get('profile_url')
        try:
            organizer = Organizer.objects.get(profile_url=profile_url)
            self.user = organizer.user
        except Organizer.DoesNotExist:
            return False
        return True

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

    def get_queryset(self):
        return self.user.user_reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            user=self.user,
            author=self.request.user,
        )


class ReviewRUDView(generics.RetrieveUpdateDestroyAPIView):
    """ Review Retrieve Update Destroy View """
    permission_classes = [IsAuthenticated, UserIsAuthor]
    lookup_field = 'uuid'
    queryset = Review.objects.all()
    serializer_class = ReviewRUDSerializer
