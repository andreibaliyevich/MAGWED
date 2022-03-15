from django.urls import path
from . import views


app_name = 'social'

urlpatterns = [    
    path('notifications/', views.NotificationListView.as_view()),
    path('comment/create/', views.CommentCreateView.as_view()),
]
