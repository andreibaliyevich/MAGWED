from django.urls import path, include
from . import views


app_name = 'portfolio'

urlpatterns = [
    path('album/', include([
        path('owner/', include([
            path('list-create/', views.AlbumListCreateView.as_view()),
            path('image-update/<uuid:uuid>/',
                views.AlbumImageUpdateView.as_view()),
            path('rud/<uuid:uuid>/', views.AlbumRUDView.as_view()),
        ])),
        path('list/', views.AlbumListView.as_view()),
        path('retrieve/<uuid:uuid>/', views.AlbumRetrieveView.as_view()),
        path('up-view-count/', views.AlbumUpViewCountView.as_view()),
        path('like/', views.AlbumLikeView.as_view()),
    ])),

    path('photo/', include([
        path('owner/', include([
            path('list-create/', views.PhotoListCreateView.as_view()),
            path('rud/<uuid:uuid>/', views.PhotoRUDView.as_view()),
        ])),
        path('list/', views.PhotoListView.as_view()),
        path('retrieve/<uuid:uuid>/', views.PhotoRetrieveView.as_view()),
        path('up-view-count/', views.PhotoUpViewCountView.as_view()),
        path('like/', views.PhotoLikeView.as_view()),
    ])),
]
