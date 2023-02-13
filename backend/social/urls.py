from django.urls import path, include
from . import views


app_name = 'social'

urlpatterns = [
    path('links/', include([
        path('', views.SocialLinkListCreateView.as_view()),
        path('<uuid:uuid>/', views.SocialLinkRUDView.as_view()),
    ])),
    path('comments/', include([
        path('<str:content_type>/<int:object_uuid>/',
            views.CommentListCreateView.as_view()),
        path('<uuid:uuid>/', views.CommentRUDView.as_view()),
    ])),
    path('reviews/', include([
        path('organizer/<slug:profile_url>/',
            views.ReviewListCreateView.as_view()),
        path('<uuid:uuid>/', views.ReviewRUDView.as_view()),
    ])),
]
