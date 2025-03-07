from django.shortcuts import get_object_or_404, get_list_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Reservation
from customers.models import Customer
from tables.models import Table

@csrf_exempt
def create_reservation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        customer_id = data.get('customer')
        table_id = data.get('table')
        date = data.get('date')

        customer = get_object_or_404(Customer, id=customer_id)
        table = get_object_or_404(Table, id=table_id)

        if Reservation.objects.filter(table=table, date=date).exists():
            return JsonResponse({'error': 'Этот столик уже забронирован на эту дату'}, status=400)

        if Reservation.objects.filter(customer=customer, date=date).exists():
            return JsonResponse({'error': 'У клиента уже есть бронь на эту дату'}, status=400)

        reservation = Reservation.objects.create(customer=customer, table=table, date=date, status="ожидает")
        return JsonResponse({'message': 'Бронь успешно создана', 'reservation_id': reservation.id})

def get_reservation_details(request, id):
    reservation = get_object_or_404(Reservation, id=id)
    data = {
        'id': reservation.id,
        'customer': reservation.customer.name,
        'table': reservation.table.number,
        'date': reservation.date.strftime('%Y-%m-%d'),
        'status': reservation.status
    }
    return JsonResponse(data)

def get_reservations_by_customer(request, customer_id):
    reservations = get_list_or_404(Reservation, customer_id=customer_id)
    data = [{'id': res.id, 'table': res.table.number, 'date': res.date.strftime('%Y-%m-%d'), 'status': res.status} for res in reservations]
    return JsonResponse({'reservations': data})

@csrf_exempt
def update_reservation_status(request, id):
    if request.method == 'POST':
        data = json.loads(request.body)
        status = data.get('status')

        if status not in ["ожидает", "подтверждено", "отменено"]:
            return JsonResponse({'error': 'Неверный статус бронирования'}, status=400)

        reservation = get_object_or_404(Reservation, id=id)
        reservation.status = status
        reservation.save()

        return JsonResponse({'message': 'Статус бронирования обновлен'})

@csrf_exempt
def delete_reservation(request, id):
    if request.method == 'DELETE':
        reservation = get_object_or_404(Reservation, id=id)
        reservation.delete()
        return JsonResponse({'message': 'Бронь удалена'}, status=204)
