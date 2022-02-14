from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('article/upload/image/',
        views.article_upload_image,
        name='article_upload_image'),
]
