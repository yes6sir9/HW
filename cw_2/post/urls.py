from django.urls import path
from . import views
from .views import post_create


urlpatterns = [
    path('', views.post_list, name='post_list'), 
    path('posts/', views.post_list, name='post_list'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/new/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('create/', post_create, name='post_create'),

]