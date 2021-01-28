from django.contrib.auth import views as auth_views
from django.urls import include, path

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('rate/', include('rate_jokes.urls')),
]
