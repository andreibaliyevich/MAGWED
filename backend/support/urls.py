from django.urls import path
from . import views


urlpatterns = [
    path('feedback/', views.FeedbackCreateView.as_view()),
    path('report/', views.ReportCreateView.as_view()),
]
