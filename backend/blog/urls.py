from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<slug:slug>/',
        views.CategoryDetailView.as_view(),
        name='category_detail'),

    path('articles/', views.ArticleListView.as_view(), name='article_list'),
    path('articles/<slug:slug>/',
        views.ArticleDetailView.as_view(),
        name='article_detail'),

    path('article/upload/image/',
        views.article_upload_image,
        name='article_upload_image'),
]
