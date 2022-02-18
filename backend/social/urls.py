from django.urls import path
from . import views


app_name = 'social'

urlpatterns = [    
    path('notifications/',
        views.NotificationListView.as_view(),
        name='notification_list'),
    path('comment/create/<str:obj_type>/<int:obj_id>/',
        views.CommentCreateView.as_view(),
        name='comment_create'),
]
