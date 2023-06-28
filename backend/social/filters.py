from django_filters import rest_framework as filters
from .models import Follow, Review


class FollowFilter(filters.FilterSet):
    """ Follow Filter """

    class Meta:
        model = Follow
        fields = [
            'follower',
            'user',
        ]

class ReviewFilter(filters.FilterSet):
    """ Review Filter """

    class Meta:
        model = Review
        fields = ['user']
