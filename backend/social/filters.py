from django_filters import rest_framework as filters
from .models import Follow


class FollowFilter(filters.FilterSet):
    """ Follow Filter """

    class Meta:
        model = Follow
        fields = [
            'follower',
            'user',
        ]