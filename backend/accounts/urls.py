from django.urls import path, include
from . import views


app_name = 'accounts'

urlpatterns = [
    path('auth/', include([
        path('login/', views.LoginView.as_view()),
        path('logout/', views.LogoutView.as_view()),
        path('registration/', views.RegistrationView.as_view()),
        path('activation/', views.ActivationView.as_view()),
        path('password/', include([
            path('change/', views.PasswordChangeView.as_view()),
        ])),
    ])),

    path('organizers/', include([
        path('', views.OrganizerListView.as_view()),
        path('<slug:profile_url>/', views.OrganizerDetailView.as_view()),
    ])),
]
