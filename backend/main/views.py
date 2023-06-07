from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from .filters import CityFilter
from .models import City, Magazine
from .serializers import CitySerializer, MagazineSerializer


class CityListView(generics.ListAPIView):
    """ City List View """
    permission_classes = [AllowAny]
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CityFilter


class MagazineView(APIView):
    """ Magazine View """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        obj = Magazine.objects.last()
        serializer = MagazineSerializer(obj, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


def error_400(request, exception):
    """ Error 400 """
    return render(request, 'errors/400.html', status=400)


def error_403(request, exception):
    """ Error 403 """
    return render(request, 'errors/403.html', status=403)


def error_404(request, exception):
    """ Error 404 """
    return render(request, 'errors/404.html', status=404)


def error_500(request):
    """ Error 500 """
    return render(request, 'errors/500.html', status=500)
