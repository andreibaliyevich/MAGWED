from django.urls import path, include
from . import views


app_name = 'messenger'

urlpatterns = [
    path('chats/', include([
        path('', views.ChatListView.as_view()),
        path('<uuid:uuid>/', views.ChatRetrieveView.as_view()),
    ])),
    path('messages/', include([
        path('', views.MessageListView.as_view()),
        path('text/', views.TextMessageView.as_view()),
        path('images/', views.ImageMessageView.as_view()),
        path('files/', views.FileMessageView.as_view()),
    ])),
]
