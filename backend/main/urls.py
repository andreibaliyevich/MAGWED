from django.urls import path
from . import views


urlpatterns = [
    path('cities/', views.CityListView.as_view()),
    path('magazine/', views.MagazineView.as_view()),
    path('tag/<uuid:uuid>/', views.TagRetrieveView.as_view()),
]
