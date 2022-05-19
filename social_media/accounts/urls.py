from django.contrib import admin
from django.urls import path, include
from .views import SignupView,LoginView,ResetPasswordView,UserDetailsView
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/',LoginView.as_view(),name='login'),
    path('reset/',ResetPasswordView.as_view(),name='reset_password'),
    path('users/<str:username>',UserDetailsView.as_view(),name='users'),
]