from django.urls import path, include
from . import views


app_name = 'reviews'

urlpatterns = [
    path('', views.ReviewListCreateView.as_view()),
    path('<uuid:uuid>/', views.ReviewUpdateDestroyView.as_view()),
]
