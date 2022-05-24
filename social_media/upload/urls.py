from django.contrib import admin
from django.urls import path, include
from .views import PostView, UploadView

urlpatterns = [
    path('upload/', UploadView.as_view(), name='upload_post'),
    # this end point will update and delete and return single post corresponding to post id
    path('post/<post_id>', PostView.as_view(), name='post'),

]
