from django.urls import path
from . import views


app_name = 'portfolio'

urlpatterns = [
    path('albums/', views.AlbumListView.as_view(), name='album_list'),
    path('albums/<int:pk>/',
        views.AlbumDetailView.as_view(),
        name='album_detail'),

    path('photos/', views.PhotoListView.as_view(), name='photo_list'),
    path('photos/<int:pk>/',
        views.PhotoDetailView.as_view(),
        name='photo_detail'),
]
