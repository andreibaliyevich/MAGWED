from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from .models import Country, City, Language
from .serializers import (
    CountryListSerializer,
    CityListSerializer,
    LanguageListSerializer,
)


class CountryListView(APIView):
    """ Country List View """

    def get(self, request):
        countries = Country.objects.all()
        serializer = CountryListSerializer(countries, many=True)
        return Response(serializer.data)


class CityListView(APIView):
    """ City List View """

    def get(self, request):
        cities = City.objects.all()
        serializer = CityListSerializer(cities, many=True)
        return Response(serializer.data)


class LanguageListView(APIView):
    """ Language List View """

    def get(self, request):
        languages = Language.objects.all()
        serializer = LanguageListSerializer(languages, many=True)
        return Response(serializer.data)


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
