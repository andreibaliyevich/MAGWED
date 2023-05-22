from django.urls import path, include
from . import views


app_name = 'portfolio'

urlpatterns = [
    path('albums/', include([
        path('crud/', include([
            path('', views.AlbumListCreateView.as_view()),
            path('<uuid:uuid>/image/', views.AlbumImageUpdateView.as_view()),
            path('<uuid:uuid>/', views.AlbumRUDView.as_view()),
        ])),
        path('list/', views.AlbumListView.as_view()),
        path('detail/', views.AlbumDetailView.as_view()),
    ])),

    path('photos/', include([
        path('crud/', include([
            path('', views.PhotoListCreateView.as_view()),
            path('<uuid:uuid>/', views.PhotoRUDView.as_view()),
        ])),
        path('list/', views.PhotoListView.as_view()),
        path('detail/', views.PhotoDetailView.as_view()),
    ])),
]
