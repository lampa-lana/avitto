from django.urls import path
from django.urls.base import reverse_lazy
from .views_auth import (MyLoginView, SignUpView, logout_view,
                         EditProfileView, ProfileView, AllProfileView)

from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetCompleteView,
    PasswordResetConfirmView)


# app_name = 'core'

urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile'),
    path('profiles/', AllProfileView.as_view(), name='all_profile'),
    path('profile/<int:user_id>/edit/',
         EditProfileView.as_view(), name='edit_profile'),
    path('sighup/', SignUpView.as_view(), name='sighup'),

    path('password_reset/', PasswordResetView.as_view(
        success_url=reverse_lazy('core:password_reset_done'),
        template_name='my_auth/password_reset.html',
        email_template_name='my_auth/password_reset_email.html'),
        name='password_reset'),

    path('password_reset/done/',
         PasswordResetDoneView.as_view(template_name='my_auth/password_reset_done.html'), name='password_reset_done'),

    path('password_reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('core:password_reset_complete'), template_name='my_auth/password_reset_confirm.html'),
        name='password_reset_confirm'),

    path('password_reset/complete/', PasswordResetCompleteView.as_view(template_name='my_auth/password_reset_complete.html'),
         name='password_reset_complete'),
]
