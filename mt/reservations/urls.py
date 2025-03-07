from django.urls import path
from .views import (
    create_reservation, get_reservation_details, get_reservations_by_customer,
    update_reservation_status, delete_reservation
)

urlpatterns = [
    path('', create_reservation, name='create_reservation'),
    path('<int:id>/', get_reservation_details, name='get_reservation_details'),
    path('customer/<int:customer_id>/', get_reservations_by_customer, name='get_reservations_by_customer'),
    path('<int:id>/update/', update_reservation_status, name='update_reservation_status'),
    path('<int:id>/delete/', delete_reservation, name='delete_reservation'),
]
