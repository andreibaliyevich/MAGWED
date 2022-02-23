from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('countries/',
        views.CountryListView.as_view(),
        name='country_list'),
    path('cities/',
        views.CityListView.as_view(),
        name='city_list'),
    path('languages/',
        views.LanguageListView.as_view(),
        name='language_list'),
    path('hashtags/',
        views.HashtagListView.as_view(),
        name='hashtag_list'),
]
