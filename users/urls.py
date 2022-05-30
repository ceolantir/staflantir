from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    MyRegistrationView,
    MyLoginView,
    ProfileView,
    ChangePasswordView,
)

urlpatterns = [
    path('registration/', MyRegistrationView.as_view(), name='reg'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('myprofile/', ProfileView.as_view(), name='profile'),
    path('profile/change/password/', ChangePasswordView.as_view(), name='change_password'),
]
