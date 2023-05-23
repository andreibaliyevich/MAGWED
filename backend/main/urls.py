from django.urls import path
from . import views


app_name = 'main'

urlpatterns = [
    path('cities/', views.CityListView.as_view()),
    path('magazine/', views.MagazineView.as_view()),
]
