from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Tag
from .serializers import TagListSerializer


class TagsListView(generics.ListAPIView):
    """ Tag List View """
    permission_classes = [AllowAny]
    queryset = Tag.objects.all()
    serializer_class = TagListSerializer
