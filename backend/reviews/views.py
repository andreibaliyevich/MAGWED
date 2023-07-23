from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ReviewFilter
from .models import Review
from .pagination import ReviewPagination
from .permissions import UserIsAuthor
from .serializers import ReviewListCreateSerializer, ReviewRUDSerializer


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
