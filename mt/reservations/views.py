
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationForm
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Reservation
from tables.models import Table
import json


def create_reservation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        customer_id = data["customer_id"]
        table_id = data["table_id"]
        date = data["date"]

        
        existing_reservation = Reservation.objects.filter(table_id=table_id, date=date).exists()
        if existing_reservation:
            return JsonResponse({"error": "Table is already booked on this date"}, status=400)

        
        user_existing_reservation = Reservation.objects.filter(customer_id=customer_id, date=date).exists()
        if user_existing_reservation:
            return JsonResponse({"error": "You already have a reservation on this date"}, status=400)

    
        reservation = Reservation.objects.create(customer_id=customer_id, table_id=table_id, date=date, status="confirmed")

        
        table = Table.objects.get(id=table_id)
        table.is_available = False
        table.save()

        return JsonResponse({
            "id": reservation.id,
            "customer": reservation.customer.name,
            "table": f"Table {reservation.table.number}",
            "date": reservation.date,
            "status": reservation.status
        })

def reservation_list(request):
    reservations = Reservation.objects.all()
    return render(request, 'reservations/reservations_list.html', {'reservations': reservations})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Reservation



def delete_reservation(request, id):  
    reservation = get_object_or_404(Reservation, id=id)

    if request.method == "POST":
        reservation.delete()
        return redirect('reservations_list')

    return render(request, 'reservations/delete_reservation.html', {'reservation': reservation})



def add_reservation(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reservations_list')
    else:
        form = ReservationForm()
    return render(request, 'reservations/add_reservation.html', {'form': form})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Reservation
from .forms import ReservationForm


def edit_reservation(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    if request.method == "POST":
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('reservations_list')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'reservations/edit_reservation.html', {'form': form, 'reservation': reservation})
