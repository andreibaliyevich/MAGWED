from rest_framework import generics
from django.shortcuts import render
from .models import Country, City, Language, Hashtag
from .serializers import (
    CountrySerializer,
    CitySerializer,
    LanguageSerializer,
    HashtagSerializer,
)


class CountryListView(generics.ListAPIView):
    """ Country List View """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityListView(generics.ListAPIView):
    """ City List View """
    queryset = City.objects.all()
    serializer_class = CitySerializer


class LanguageListView(generics.ListAPIView):
    """ Language List View """
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class HashtagListView(generics.ListAPIView):
    """ Hashtag List View """
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer


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
