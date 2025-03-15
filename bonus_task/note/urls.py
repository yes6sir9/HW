from django.urls import path
from . import views

urlpatterns = [
    path('', views.note_list, name='note_list'),
    path('note/<int:note_id>/', views.note_detail, name='note_detail'),
    path('note/new/', views.note_create, name='note_create'),
    path('note/<int:note_id>/edit/', views.note_update, name='note_update'),
    path('note/<int:note_id>/delete/', views.note_delete, name='note_delete'),
]
