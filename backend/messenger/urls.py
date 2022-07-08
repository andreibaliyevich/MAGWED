from django.urls import path
from . import views


app_name = 'messenger'

urlpatterns = [
    path('conversations/', views.ConversationListView.as_view()),
]
