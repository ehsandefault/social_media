from django.urls import path
from .views import FollowView
urlpatterns = [
path('follow/<str:user_name>',FollowView.as_view(),name='follow')
]