from django.urls import path, include
from . import views


app_name = 'blog'

urlpatterns = [
    path('article/', include([
        path('list/', views.ArticleListView.as_view()),
        path('retrieve/<slug:slug>/', views.ArticleRetrieveView.as_view()),
        path('up-view-count/<slug:slug>/',
            views.ArticleUpViewCountView.as_view()),
    ])),
    path('upload/image/', views.upload_image),
]
