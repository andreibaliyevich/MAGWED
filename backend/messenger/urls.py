from django.urls import path, include
from . import views


app_name = 'messenger'

urlpatterns = [
    path('chat/', include([
        path('list/', views.ChatListView.as_view()),
        path('retrieve/<uuid:uuid>/', views.ChatRetrieveView.as_view()),
    ])),
    path('message/', include([
        path('list/', views.MessageListView.as_view()),
        path('text/', views.TextMessageView.as_view()),
        path('images/', views.ImageMessageView.as_view()),
        path('files/', views.FileMessageView.as_view()),
        path('write/', views.WriteMessageView.as_view()),
    ])),
]
