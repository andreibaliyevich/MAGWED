from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.ReviewListCreateView.as_view()),
    path('<uuid:uuid>/', views.ReviewUpdateDestroyView.as_view()),
]
