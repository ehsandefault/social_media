from django.contrib import admin
from django.urls import path, include
from .views import PostView

urlpatterns = [
    path('upload/',PostView.as_view(),name='upload_post'),
    path('edit/<post_id>',PostView.as_view(),name='edit_post'),
    path('delete/<post_id>',PostView.as_view(),name='delete_post'),

]