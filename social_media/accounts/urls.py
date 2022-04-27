from django.contrib import admin
from django.urls import path, include
from .views import SignupView,Login,ResetPassword,UserDetailsView
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/',Login.as_view(),name='login'),
    path('reset_password/',ResetPassword.as_view(),name='reset_password'),
    path('users_profile/<str:username>',UserDetailsView.as_view(),name='users_profile'),
]