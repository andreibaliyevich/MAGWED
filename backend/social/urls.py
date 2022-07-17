from django.urls import path, include
from . import views


app_name = 'social'

urlpatterns = [    
    path('notifications/', views.NotificationListView.as_view()),

    path('comments/', include([
        path('<str:content_type>/<int:object_id>/',
            views.CommentListCreateView.as_view()),
        path('<int:pk>/', views.CommentRUDView.as_view()),
    ])),
]
