from django.shortcuts import get_list_or_404
from django.http import JsonResponse
from .models import Table
from reservations.models import Reservation

def available_tables(request):
    date = request.GET.get('date')
    if not date:
        return JsonResponse({'error': 'Дата не указана'}, status=400)

    reserved_tables = Reservation.objects.filter(date=date).values_list('table_id', flat=True)
    available_tables = Table.objects.exclude(id__in=reserved_tables).filter(available=True)

    tables_list = list(available_tables.values())
    return JsonResponse({'available_tables': tables_list})
