from django.urls import path
from .views import available_tables

urlpatterns = [
    path('available/', available_tables, name='available_tables'),
]
