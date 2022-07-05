from django.urls import path
from . import views


app_name = 'messenger'

urlpatterns = [
    path('chats/', views.ChatListView.as_view()),
]
