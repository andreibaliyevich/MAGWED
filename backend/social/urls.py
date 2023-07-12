from django.urls import path, include
from . import views


app_name = 'social'

urlpatterns = [
    path('links/', include([
        path('', views.SocialLinkListCreateView.as_view()),
        path('<uuid:uuid>/', views.SocialLinkRUDView.as_view()),
    ])),
    path('follow/', include([
        path('', views.FollowCreateDestroyView.as_view()),
        path('list/', views.FollowListView.as_view()),
    ])),
    path('favorite/', include([
        path('', views.FavoriteCreateDestroyView.as_view()),
        path('list/', views.FavoriteListView.as_view()),
    ])),
    path('reviews/', include([
        path('', views.ReviewListCreateView.as_view()),
        path('<uuid:uuid>/', views.ReviewRUDView.as_view()),
    ])),
    path('comments/', include([
        path('', views.CommentListCreateView.as_view()),
        path('<uuid:uuid>/', views.CommentRUDView.as_view()),
    ])),
]
