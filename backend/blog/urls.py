from django.urls import path, include
from . import views


app_name = 'blog'

urlpatterns = [
    path('categories/', include([
        path('', views.CategoryListView.as_view()),
        path('<slug:slug>/', views.CategoryDetailView.as_view()),
    ])),

    path('articles/', include([
        path('', views.ArticleListView.as_view()),
        path('<slug:slug>/', views.ArticleDetailView.as_view()),
    ])),

    path('article/upload/image/', views.article_upload_image),
]
