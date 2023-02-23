from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('countries/', views.CountryListView.as_view()),
    path('cities/', views.CityListView.as_view()),
    path('languages/', views.LanguageListView.as_view()),
    path('magazine/', views.MagazineView.as_view()),
]
