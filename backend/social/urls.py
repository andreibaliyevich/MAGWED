from django.urls import path, include
from . import views


app_name = 'social'

urlpatterns = [
    path('links/', include([
        path('', views.SocialLinkListCreateView.as_view()),
        path('<uuid:uuid>/', views.SocialLinkRUDView.as_view()),
    ])),
    path('follow/', include([
        path('', views.FollowView.as_view()),
        path('list/', views.FollowListView.as_view()),
    ])),
    path('reviews/', include([
        path('', views.ReviewListCreateView.as_view()),
        path('<uuid:uuid>/', views.ReviewRUDView.as_view()),
    ])),
    path('comments/', include([
        path('<str:content_type>/<uuid:object_uuid>/',
            views.CommentListCreateView.as_view()),
        path('<uuid:uuid>/', views.CommentRUDView.as_view()),
    ])),
]
