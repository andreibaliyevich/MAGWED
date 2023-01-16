from django.urls import path, include
from . import views


app_name = 'social'

urlpatterns = [    
    path('comments/', include([
        path('<str:content_type>/<int:object_id>/',
            views.CommentListCreateView.as_view()),
        path('<int:pk>/', views.CommentRUDView.as_view()),
    ])),
    path('reviews/', include([
        path('organizer/<slug:profile_url>/',
            views.ReviewListCreateView.as_view()),
        path('<int:pk>/', views.ReviewRUDView.as_view()),
    ])),
]
