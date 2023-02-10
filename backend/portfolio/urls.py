from django.urls import path, include
from . import views


app_name = 'portfolio'

urlpatterns = [
    path('albums/', include([
        path('', views.AlbumListCreateView.as_view()),
        path('<uuid:uuid>/', views.AlbumRUDView.as_view()),
    ])),

    path('photos/', include([
        path('', views.PhotoListCreateView.as_view()),
        path('<uuid:uuid>/', views.PhotoRUDView.as_view()),
    ])),
]
