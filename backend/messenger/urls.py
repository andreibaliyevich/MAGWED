from django.urls import path, include
from . import views


app_name = 'messenger'

urlpatterns = [
    path('conversations/', views.ConversationListView.as_view()),
    path('message/', include([
        path('images/', views.ImageMessageView.as_view()),
        path('files/', views.FileMessageView.as_view()),
    ])),
]
