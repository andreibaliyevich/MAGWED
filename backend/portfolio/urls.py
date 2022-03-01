from django.urls import path, include
from . import views


app_name = 'portfolio'

urlpatterns = [
    path('albums/', include([
        path('', views.AlbumListView.as_view()),
        path('<int:pk>/', views.AlbumDetailView.as_view()),
    ])),

    path('photos/', include([
        path('', views.PhotoListView.as_view()),
        path('<int:pk>/', views.PhotoDetailView.as_view()),
    ])),
]
