from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import AccountView, upgrade_me


urlpatterns = [
    path('account/', AccountView.as_view()),
    path('upgrade/', upgrade_me, name='upgrade'),
]