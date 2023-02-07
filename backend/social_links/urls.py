from django.urls import path
from . import views


app_name = 'social_links'

urlpatterns = [
    path('', views.SocialLinkListCreateView.as_view()),
    path('<int:pk>/', views.SocialLinkRUDView.as_view()),
]
