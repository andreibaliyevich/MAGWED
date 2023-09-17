from django.urls import path, include
from . import views


app_name = 'messenger'

urlpatterns = [
    path('chat/', include([
        path('list/', views.ChatListView.as_view()),
        path('create/', views.ChatCreateView.as_view()),
        path('retrieve/<uuid:uuid>/', views.ChatRetrieveView.as_view()),
        path('group-retrieve/<uuid:uuid>/',
            views.GroupChatRetrieveView.as_view()),
        path('destroy/<uuid:uuid>/', views.ChatDestroyView.as_view()),
        path('leave/<uuid:uuid>/', views.ChatLeaveView.as_view()),
    ])),
    path('message/', include([
        path('list/', views.MessageListView.as_view()),
        path('text/', views.TextMessageView.as_view()),
        path('images/', views.ImageMessageView.as_view()),
        path('files/', views.FileMessageView.as_view()),
        path('write/', views.WriteMessageView.as_view()),
    ])),
]
