from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from accounts.permissions import UserIsOrganizer
from accounts.serializers import UserUUIDSerializer, UserBriefReadSerializer
from .filters import FollowFilter, FavoriteFilter
from .models import SocialLink, Follow, Favorite
from .pagination import (
    FollowPagination,
    FavoritePagination,
)
from .serializers import (
    SocialLinkSerializer,
    FollowersSerializer,
    FollowingSerializer,
    FavoriteContentObjectSerializer,
    FavoriteListSerializer,
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


class SocialLinkUpdateDestroyView(
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        generics.GenericAPIView):
    """ Social Link Update Destroy View """
    permission_classes = [IsAuthenticated, UserIsOrganizer]
    lookup_field = 'uuid'
    serializer_class = SocialLinkSerializer

    def get_queryset(self):
        return SocialLink.objects.filter(user=self.request.user)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


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


class RelatedUsersView(APIView):
    """ Related Users View """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        following_uuid = request.user.following.values_list(
            'user__uuid',
            flat=True,
        )
        followers_uuid = request.user.followers.values_list(
            'follower__uuid',
            flat=True,
        )
        queryset = UserModel.objects.filter(
            Q(uuid__in=following_uuid) | Q(uuid__in=followers_uuid)
        )
        serializer = UserBriefReadSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FavoriteListView(generics.ListAPIView):
    """ Favorite List View """
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteListSerializer
    pagination_class = FavoritePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = FavoriteFilter

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
