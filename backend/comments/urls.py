from django.urls import path, include
from . import views


app_name = 'comments'

urlpatterns = [
    path('', views.CommentListCreateView.as_view()),
    path('<uuid:uuid>/', views.CommentUpdateDestroyView.as_view()),
]
