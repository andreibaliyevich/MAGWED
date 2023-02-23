from django.urls import path
from . import views


app_name = 'tags'

urlpatterns = [    
    path('', views.TagsListView.as_view()),
]
