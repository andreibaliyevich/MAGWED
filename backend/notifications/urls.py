from django.urls import path
from . import views


urlpatterns = [    
    path('', views.NotificationListView.as_view()),
    path('list-destroy/', views.NotificationListDestroyView.as_view()),
]
