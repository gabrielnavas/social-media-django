from django.urls import path

from . import views

urlpatterns = [
    path('', views.feed, name='feed'),
    path('create_post', views.create_post, name='create_post')
]