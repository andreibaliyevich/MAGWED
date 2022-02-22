from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('organizers/',
        views.OrganizerListView.as_view(),
        name='organizer_list'),
    path('organizers/<slug:profile_url>/',
        views.OrganizerDetailView.as_view(),
        name='organizer_detail'),
]
