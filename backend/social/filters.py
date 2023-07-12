from django_filters import rest_framework as filters
from .models import Follow, Favorite, Review, Comment


class FollowFilter(filters.FilterSet):
    """ Follow Filter """

    class Meta:
        model = Follow
        fields = [
            'follower',
            'user',
        ]


class FavoriteFilter(filters.FilterSet):
    """ Favorite Filter """

    class Meta:
        model = Favorite
        fields = ['content_type__model']


class ReviewFilter(filters.FilterSet):
    """ Review Filter """

    class Meta:
        model = Review
        fields = ['user']


class CommentFilter(filters.FilterSet):
    """ Comment Filter """

    class Meta:
        model = Comment
        fields = [
            'content_type__model',
            'object_uuid',
        ]
