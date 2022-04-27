from django.contrib import admin
from django.urls import path, include
from .views import SignupView,Login,ResetPassword,UserDetailsView
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/',Login.as_view(),name='login'),
    path('reset/',ResetPassword.as_view(),name='reset_password'),
    path('users/<str:username>',UserDetailsView.as_view(),name='users'),
]