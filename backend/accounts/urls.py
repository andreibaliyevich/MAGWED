from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from . import views


app_name = 'accounts'

urlpatterns = [
    path('auth/', include([
        path('token/', obtain_auth_token),
    ])),

    path('organizers/',
        views.OrganizerListView.as_view(),
        name='organizer_list'),
    path('organizers/<slug:profile_url>/',
        views.OrganizerDetailView.as_view(),
        name='organizer_detail'),
]
